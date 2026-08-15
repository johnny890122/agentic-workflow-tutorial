"""Unit tests for public_goods_simple's payoff rule.

set_payoffs() reads and writes ORM fields, so these run against a real session
built by the conftest fixture rather than plain objects.
"""

import pytest

from public_goods_simple import C, set_payoffs


@pytest.fixture
def group(public_goods_session):
    (subsession,) = public_goods_session.get_subsessions()
    (group,) = subsession.get_groups()
    return group


def contribute(group, amounts):
    for player, amount in zip(group.get_players(), amounts):
        player.contribution = amount
    set_payoffs(group)


def test_total_contribution_is_the_sum(group):
    contribute(group, [10, 20, 30])
    assert group.total_contribution == 60


def test_share_is_the_multiplied_pot_split_evenly(group):
    contribute(group, [10, 20, 30])
    assert group.individual_share == 60 * C.MULTIPLIER / C.PLAYERS_PER_GROUP


def test_payoff_is_what_you_kept_plus_your_share(group):
    contribute(group, [10, 20, 30])
    shares = [p.payoff for p in group.get_players()]
    assert shares == [
        C.ENDOWMENT - amount + group.individual_share for amount in [10, 20, 30]
    ]


def test_free_rider_out_earns_the_full_contributor(group):
    contribute(group, [0, C.ENDOWMENT, C.ENDOWMENT])
    free_rider, contributor, _ = group.get_players()
    assert free_rider.payoff > contributor.payoff


def test_contributing_everything_beats_contributing_nothing_for_the_group(group):
    contribute(group, [C.ENDOWMENT] * C.PLAYERS_PER_GROUP)
    all_in = sum(p.payoff for p in group.get_players())

    contribute(group, [0] * C.PLAYERS_PER_GROUP)
    none = sum(p.payoff for p in group.get_players())

    # The multiplier is > 1, so cooperating grows the pie.
    assert all_in > none


def test_contributing_alone_loses_money_for_the_contributor(group):
    """MULTIPLIER / PLAYERS_PER_GROUP < 1, which is what makes this a dilemma."""
    contribute(group, [C.ENDOWMENT, 0, 0])
    contributor = group.get_players()[0]
    assert contributor.payoff < C.ENDOWMENT
