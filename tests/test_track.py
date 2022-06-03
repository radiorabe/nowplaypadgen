"""Test :class:`Track`."""

import mock
import pytest

from nowplaypadgen.timeperiod import TimePeriod
from nowplaypadgen.track import Track


@pytest.fixture(name="track_artist")
def fixture_track_artist():
    """Track artist fixture."""
    return "My Track Artist"


@pytest.fixture(name="track_title")
def fixture_track_title():
    """Track title fixture."""
    return "My Track Title"


@pytest.fixture(name="track")
def fixture_track(track_artist, track_title):
    """Track fixture."""
    return Track(track_artist, track_title)


def test_track_supports_timeperiod(track):
    """Test that the track is an instance of TimePeriod."""

    # Test that the track inherits TimePeriod, otherwise the track lacks
    # the duration, start and end time/date methods.
    assert isinstance(track, TimePeriod)


def test_track_artist_title_assign(track_artist, track_title, track):
    """Test the track artist and title assignment."""

    assert track_artist == track.artist
    assert track_title == track.title


def test_track_string_rep(track):
    """Test the track string representation."""

    expected_string = f"Track: {track.artist} - {track.title} ({track.uuid})"
    assert expected_string == str(track)


@mock.patch("mutagen.File")
def test_track_from_file(mock_mutagen_file, track_title):
    """Test the track creation from a file."""

    # mock getting artist and title from the file
    mock_mutagen_file.return_value.get.return_value = (track_title,)
    # mock audio_file.info.length
    mock_mutagen_file.return_value.info.length = 123
    # mock getting items from the file
    mock_mutagen_file.return_value.items.return_value = [
        ("artist", "artist"),
        ("title", ["title 1, title 2"]),
    ]

    track = Track.from_file("/path/to/my/track.mp3")

    mock_mutagen_file.assert_called_once_with("/path/to/my/track.mp3")
    assert track_title == track.title
