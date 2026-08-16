"""Unit tests for the neighbourhood payoff rule (REQ-0001 rule 8).

set_payoffs() reads and writes ORM fields, so these run against a real session
built by the conftest fixture rather than plain objects.

Adjacency is set by hand rather than drawn, so the arithmetic is tested
independently of the arrangement the app happens to use. That is what let this
module be written before the arrangement was chosen.
"""

import pytest

from network_public_goods import C, set_payoffs

# id_in_group -> the ids it is linked to.
RING = {1: [2, 4], 2: [1, 3], 3: [2, 4], 4: [1, 3]}
# K4 minus the 3-4 edge: players 1 and 2 have three links, players 3 and 4 two.
DIAMOND = {1: [2, 3, 4], 2: [1, 3, 4], 3: [1, 2], 4: [1, 2]}


@pytest.fixture
def group(otree_session_factory):
    session = otree_session_factory("network_public_goods", num_participants=4)
    (subsession, *_) = session.get_subsessions()
    (group,) = subsession.get_groups()
    return group


def play(group, adjacency, contributions):
    """Pin the adjacency and the contributions, then resolve the round."""
    for player in group.get_players():
        player.links = ",".join(str(i) for i in adjacency[player.id_in_group])
        player.contribution = contributions[player.id_in_group]
    set_payoffs(group)
    return {player.id_in_group: player for player in group.get_players()}


def test_ring_uniform_contributions(group):
    # 30 divides evenly by the neighbourhood size of 3, so this is the
    # arithmetic with no rounding in the way: each of the three givers reaching
    # a player sends 30 * 2 / 3 = 20, so received = 60 and kept = 70.
    players = play(group, RING, {i: C.ENDOWMENT * 3 / 10 for i in RING})

    for player in players.values():
        assert player.payoff == C.ENDOWMENT * 13 / 10


def test_uneven_splits_round_and_the_group_loses_the_remainder(group):
    """Points are whole numbers, so a share that does not divide is rounded.

    REQ-0001 rule 8 says a contribution is "shared evenly", which is not
    achievable when the amount does not divide by the neighbourhood size. With
    50 contributed into a neighbourhood of 3, each share is 33 rather than
    33.33, so 1 point per contributor evaporates.

    This is asserted rather than worked around, so the behaviour is visible in
    the data and cannot change silently. See the open question on OT-0002.
    """
    players = play(group, RING, {i: C.ENDOWMENT / 2 for i in RING})

    for player in players.values():
        # 50 kept + 3 shares of 33, not 50 + 100.
        assert player.payoff == C.ENDOWMENT / 2 + (C.ENDOWMENT - C.ENDOWMENT / 100)


def test_ring_free_rider_out_earns_contributors(group):
    players = play(group, RING, {1: cu_zero(), 2: C.ENDOWMENT, 3: C.ENDOWMENT, 4: C.ENDOWMENT})

    assert players[1].payoff > players[2].payoff
    assert players[1].payoff > players[3].payoff


def test_ring_neighbours_of_a_free_rider_earn_less(group):
    players = play(group, RING, {1: cu_zero(), 2: C.ENDOWMENT, 3: C.ENDOWMENT, 4: C.ENDOWMENT})

    # On a 4-ring, 1 is linked to 2 and 4; player 3 is the only contributor not
    # linked to the free rider.
    assert players[2].payoff < players[3].payoff
    assert players[4].payoff < players[3].payoff


def test_divisor_is_the_contributors_neighbourhood(group):
    """The failure mode most likely to be implemented backwards.

    On a diamond, player 1's neighbourhood is size 4 and player 3's is size 3.
    Only player 1 contributes, so every receipt must be 100 * 2 / 4 = 50 --
    computed from the *giver's* neighbourhood. An implementation dividing by the
    receiver's would give player 3 a share of 100 * 2 / 3 instead.
    """
    players = play(
        group, DIAMOND, {1: C.ENDOWMENT, 2: cu_zero(), 3: cu_zero(), 4: cu_zero()}
    )

    share = C.ENDOWMENT * 2 / 4
    assert players[1].payoff == share  # kept nothing, receives its own share
    for receiver in (2, 3, 4):
        assert players[receiver].payoff == C.ENDOWMENT + share


def test_nobody_contributes(group):
    players = play(group, RING, {i: cu_zero() for i in RING})

    for player in players.values():
        assert player.payoff == C.ENDOWMENT


def test_full_contribution_grows_the_pie(group):
    players = play(group, RING, {i: C.ENDOWMENT for i in RING})
    all_in = sum(player.payoff for player in players.values())

    players = play(group, RING, {i: cu_zero() for i in RING})
    none = sum(player.payoff for player in players.values())

    assert all_in > none


def cu_zero():
    """C.ENDOWMENT is a Currency; multiplying by 0 keeps the type."""
    return C.ENDOWMENT * 0
