"""Test :class:`Show`."""

import pytest

from nowplaypadgen.show import Show
from nowplaypadgen.timeperiod import TimePeriod


@pytest.fixture(name="show_name")
def fixture_show_name():
    """Show name fixture."""
    return "My Show Name"


@pytest.fixture(name="show")
def fixture_show(show_name):
    """Show fixture."""
    return Show(show_name)


def test_show_supports_timeperiod(show):
    """Test that the show is an instance of timeperiod.TimePeriod."""

    # Test that the show inherits TimePeriod, otherwise the show lacks
    # the start and end time/date methods.
    assert isinstance(show, TimePeriod)


def test_show_name_assignment(show, show_name):
    """Test the show name assignment."""

    assert show_name == show.name
