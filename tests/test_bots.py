"""Runs the oTree bots (demo/<app>/tests.py) as pytest cases.

Same code path as `otree test <config>`, so bot failures surface in a normal
pytest run instead of needing a separate command.
"""

import pytest
from otree.bots.runner import run_bots
from otree.session import SESSION_CONFIGS_DICT

SESSION_CONFIG_NAMES = sorted(SESSION_CONFIGS_DICT)


@pytest.mark.parametrize("session_config_name", SESSION_CONFIG_NAMES)
def test_bots_play_through(session_config_name, otree_session_factory):
    config = SESSION_CONFIGS_DICT[session_config_name]
    session = otree_session_factory(
        session_config_name, num_participants=config["num_demo_participants"]
    )
    # Raises (AssertionError, or whatever the bot's own asserts raise) on failure.
    run_bots(session.id)
