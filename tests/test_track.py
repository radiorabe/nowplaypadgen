"""Track related unit tests."""

import os
import sys
import unittest

import mock

from nowplaypadgen import timeperiod, track

# Load the module locally from the dev environment.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class TrackTestSuite(unittest.TestCase):
    """Track test cases."""

    def setUp(self):
        self.track_artist = "My Track Artist"
        self.track_title = "My Track Title"
        self.my_track = track.Track(self.track_artist, self.track_title)

    def test_track_supports_timeperiod(self):
        """Test that the track is an instance of timeperiod.TimePeriod."""

        # Test that the track inherits TimePeriod, otherwise the track lacks
        # the duration, start and end time/date methods.
        self.assertTrue(isinstance(self.my_track, timeperiod.TimePeriod))

    def test_track_artist_title_assign(self):
        """Test the track artist and title assignment."""

        self.assertEqual(self.track_artist, self.my_track.artist)
        self.assertEqual(self.track_title, self.my_track.title)

    def test_track_string_rep(self):
        """Test the track string representation."""

        expected_string = "Track: {0} - {1} ({2})".format(
            self.my_track.artist, self.my_track.title, self.my_track.uid
        )

        self.assertEqual(expected_string, str(self.my_track))

    @mock.patch("mutagen.File")
    def test_track_from_file(self, mock_mutagen_file):
        """Test the track creation from a file."""

        # mock getting artist and title from the file
        mock_mutagen_file.return_value.get.return_value = (self.track_title,)
        # mock audio_file.info.length
        mock_mutagen_file.return_value.info.length = 123
        # mock getting items from the file
        mock_mutagen_file.return_value.items.return_value = [
            ("artist", "artist"),
            ("title", ["title 1, title 2"]),
        ]

        my_track = track.Track.from_file("/path/to/my/track.mp3")

        mock_mutagen_file.assert_called_once_with("/path/to/my/track.mp3")
        self.assertEqual("My Track Title", my_track.title)


if __name__ == "__main__":
    unittest.main()
