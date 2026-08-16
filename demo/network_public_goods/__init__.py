"""Public goods on a network that is redrawn every round.

Implements REQ-0001. The four players are one fixed oTree group for the whole
session; what changes each round is the network *inside* that group. So this is
not a grouping problem -- `group_randomly()` would re-matter the wrong thing --
and the adjacency is drawn and stored by the app.

The arrangement is a ring, per artifacts/OT-0002-01-link-arrangements/DECISION.md.
That decision is provisional: it was made on implementation grounds because the
artifact stage could not run, not by the researcher looking at alternatives.
"""

import random

from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'network_public_goods'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 10
    ENDOWMENT = cu(100)
    MULTIPLIER = 2


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    contribution = models.CurrencyField(
        min=0, max=C.ENDOWMENT, label="How much will you contribute?"
    )
    # This round's links, as a comma-separated sorted list of id_in_group --
    # e.g. "2,4". Plain text so the data export is readable without a decoder.
    links = models.StringField()


# FUNCTIONS
def link_ids(player: Player):
    """The id_in_group values this player is linked to, this round."""
    return [int(part) for part in player.links.split(',') if part]


def neighbourhood_size(player: Player):
    """|N(i)| -- the player plus their links. The payoff divisor."""
    return 1 + len(link_ids(player))


def creating_session(subsession: Subsession):
    """Draw each round's ring before anyone reaches the decision page.

    REQ-0001 rule 6 makes the links visible at decision time, so they cannot be
    drawn on the wait page. Rule 12 requires a minimum of two links, which a
    ring satisfies unconditionally: shuffling the players into a cycle gives
    every one of them exactly two neighbours.
    """
    for group in subsession.get_groups():
        players = group.get_players()
        cycle = [player.id_in_group for player in players]
        random.shuffle(cycle)
        size = len(cycle)
        neighbours = {
            player_id: sorted([cycle[(pos - 1) % size], cycle[(pos + 1) % size]])
            for pos, player_id in enumerate(cycle)
        }
        for player in players:
            player.links = ','.join(
                str(other) for other in neighbours[player.id_in_group]
            )


def set_payoffs(group: Group):
    """REQ-0001 rule 8: a contribution is doubled, then split evenly across the
    contributor and their links.

    The divisor is the size of the *contributor's* neighbourhood, not the
    receiver's. On a ring every neighbourhood is the same size, so this
    distinction is invisible here -- it is asserted against a diamond in
    tests/test_network_public_goods_payoffs.py.
    """
    by_id = {player.id_in_group: player for player in group.get_players()}
    for player in by_id.values():
        received = sum(
            by_id[giver_id].contribution
            * C.MULTIPLIER
            / neighbourhood_size(by_id[giver_id])
            for giver_id in [player.id_in_group] + link_ids(player)
        )
        player.payoff = C.ENDOWMENT - player.contribution + received


def partner_history(player: Player):
    """One row per completed round, one column per current partner.

    REQ-0001 rule 7 wants every completed round itemised, so the worst case is
    three partners over nine rounds. A single table keeps that on one screen.
    Only the partners linked *this* round appear -- rule 10.

    Each cell also carries `was_linked`: whether this player and that partner
    were linked in that round. Without it a row reads "player 1 gave 100 in
    round 3" with no way to tell whether any of it reached you, so reciprocity
    and general generosity look identical -- see REQ-0001 rule 7 as amended.

    The flag says only whether it was *you*. It never names the partner's other
    links, which would leak information about players this viewer is not linked
    to, contrary to rule 10.
    """
    partners = [player.group.get_player_by_id(pid) for pid in link_ids(player)]
    histories = [partner.in_previous_rounds() for partner in partners]
    return [
        dict(
            round_number=index + 1,
            cells=[
                dict(
                    contribution=history[index].contribution,
                    was_linked=player.id_in_group in link_ids(history[index]),
                )
                for history in histories
            ],
        )
        for index in range(player.round_number - 1)
    ]


# PAGES
class Decide(Page):
    form_model = 'player'
    form_fields = ['contribution']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            partner_ids=link_ids(player),
            history_rows=partner_history(player),
        )


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class RoundResults(Page):
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        return dict(
            partners=[
                dict(
                    id_in_group=pid,
                    contribution=group.get_player_by_id(pid).contribution,
                )
                for pid in link_ids(player)
            ],
            kept=C.ENDOWMENT - player.contribution,
        )


page_sequence = [Decide, ResultsWaitPage, RoundResults]
