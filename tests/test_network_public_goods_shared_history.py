"""The history marker: was this partner linked to *you* in that past round?

REQ-0001 rule 7 (amended 2026-08-15). The flag is derived from the `links`
already stored for each round, so these assert the derivation rather than any
new stored field.
"""

import pytest

from network_public_goods import link_ids, partner_history


@pytest.fixture
def subsessions(otree_session_factory):
    session = otree_session_factory("network_public_goods", num_participants=4)
    return session.get_subsessions()


def set_links(subsession, adjacency):
    for player in subsession.get_players():
        player.links = ",".join(str(i) for i in adjacency[player.id_in_group])


def test_marker_is_true_only_for_rounds_the_pair_shared(subsessions):
    round1, round2, round3, *_ = subsessions

    # Round 1: player 1 linked to 2 and 4.  Round 2: linked to 3 and 4 instead,
    # so player 2 is a non-neighbour that round.  Round 3: back with 2 and 4.
    set_links(round1, {1: [2, 4], 2: [1, 3], 3: [2, 4], 4: [1, 3]})
    set_links(round2, {1: [3, 4], 2: [3, 4], 3: [1, 2], 4: [1, 2]})
    set_links(round3, {1: [2, 4], 2: [1, 3], 3: [2, 4], 4: [1, 3]})

    for subsession in (round1, round2, round3):
        for player in subsession.get_players():
            player.contribution = player.id_in_group * 10

    viewer = round3.get_players()[0]
    assert viewer.id_in_group == 1
    assert link_ids(viewer) == [2, 4]

    rows = partner_history(viewer)
    assert [row["round_number"] for row in rows] == [1, 2]

    # Column order follows link_ids: player 2 first, then player 4.
    round1_p2, round1_p4 = rows[0]["cells"]
    round2_p2, round2_p4 = rows[1]["cells"]

    assert round1_p2["was_linked"] is True   # 1-2 shared round 1
    assert round1_p4["was_linked"] is True   # 1-4 shared round 1
    assert round2_p2["was_linked"] is False  # 1 was with 3 and 4 that round
    assert round2_p4["was_linked"] is True   # 1-4 shared round 2 too


def test_contributions_are_still_reported_for_unshared_rounds(subsessions):
    """Rule 7: every completed round is shown, shared or not -- only marked."""
    round1, round2, *_ = subsessions

    set_links(round1, {1: [3, 4], 2: [3, 4], 3: [1, 2], 4: [1, 2]})
    set_links(round2, {1: [2, 4], 2: [1, 3], 3: [2, 4], 4: [1, 3]})
    for subsession in (round1, round2):
        for player in subsession.get_players():
            player.contribution = player.id_in_group * 10

    viewer = round2.get_players()[0]
    (row,) = partner_history(viewer)
    player2_cell = row["cells"][0]

    # Player 1 and 2 were not linked in round 1, but the amount is still shown.
    assert player2_cell["was_linked"] is False
    assert player2_cell["contribution"] == 20


def test_marker_never_depends_on_a_third_players_links(subsessions):
    """Rule 10: the flag reflects only the viewer-partner pair.

    Rewiring the two players the viewer is not looking at must not change any
    marker the viewer sees.
    """
    round1, round2, *_ = subsessions

    set_links(round1, {1: [2, 4], 2: [1, 3], 3: [2, 4], 4: [1, 3]})
    set_links(round2, {1: [2, 4], 2: [1, 3], 3: [2, 4], 4: [1, 3]})
    for subsession in (round1, round2):
        for player in subsession.get_players():
            player.contribution = player.id_in_group * 10

    viewer = round2.get_players()[0]
    before = [cell["was_linked"] for row in partner_history(viewer) for cell in row["cells"]]

    # Player 3 -- whom the viewer is not linked to this round -- changes partners
    # in round 1. Nothing the viewer sees may move.
    round1_players = {p.id_in_group: p for p in round1.get_players()}
    round1_players[3].links = "1,2"

    after = [cell["was_linked"] for row in partner_history(viewer) for cell in row["cells"]]
    assert before == after
