from pathlib import Path

import pytest


@pytest.fixture
def drc():
    return Path(__file__).parent
