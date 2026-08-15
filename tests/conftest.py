"""Boots oTree once per pytest run, then hands tests a real (in-memory) session.

oTree has no test-harness entry point of its own, so this replicates what the
`otree` CLI does in otree/main.py before dispatching a command: chdir into the
project folder, then call otree.main.setup() to load settings and the ORM.
"""

import os
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
PROJECT_DIR = REPO_ROOT / "demo"

# All of this must happen before the first `import otree.*`.
#
# In-memory mode keeps the run out of demo/db.sqlite3. otree.database reads
# OTREE_IN_MEMORY at import time and binds its engine right then, so setting it
# afterwards is too late.
os.environ.setdefault("OTREE_IN_MEMORY", "1")

# oTree treats the cwd as the project root and resolves a surprising amount
# against it -- `import settings`, `_static/`, app layout (otree.common.is_noself
# reads <app>/__init__.py), and page templates -- much of it lru_cached on first
# use. So run from demo/, exactly like the CLI does, rather than trying to make
# oTree location-independent.
sys.path.insert(0, str(PROJECT_DIR))
os.chdir(PROJECT_DIR)

import otree.main  # noqa: E402
from otree.database import db  # noqa: E402
from otree.session import create_session  # noqa: E402

otree.main.setup()

# Back to the repo root before pytest resolves `testpaths` and collects; the
# _otree_cwd fixture below re-enters demo/ for the duration of each test.
os.chdir(REPO_ROOT)


@pytest.fixture(autouse=True)
def _otree_cwd(monkeypatch):
    """Keep tests running under demo/, for the cwd-relative lookups noted above."""
    monkeypatch.chdir(PROJECT_DIR)


@pytest.fixture(scope="session")
def otree_session_factory():
    """Create an oTree session, the way the admin UI or the bot runner would.

    Sessions are independent rows in a shared in-memory database, so tests can
    each make their own without interfering; nothing is torn down between them.
    """

    def factory(session_config_name, num_participants=None):
        session = create_session(
            session_config_name, num_participants=num_participants
        )
        db.commit()
        return session

    return factory


@pytest.fixture
def public_goods_session(otree_session_factory):
    return otree_session_factory("public_goods_simple", num_participants=3)
