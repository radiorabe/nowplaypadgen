"""Show related unit tests."""

import unittest

from nowplaypadgen import show, timeperiod


class ShowTestSuite(unittest.TestCase):
    """Show test cases."""

    def setUp(self):
        self.show_name = "My Show Name"
        self.my_show = show.Show(self.show_name)

    def test_show_supports_timeperiod(self):
        """Test that the show is an instance of timeperiod.TimePeriod."""

        # Test that the show inherits TimePeriod, otherwise the show lacks
        # the start and end time/date methods.
        self.assertTrue(isinstance(self.my_show, timeperiod.TimePeriod))

    def test_show_name_assignment(self):
        """Test the show name assignment."""

        self.assertEqual(self.show_name, self.my_show.name)


if __name__ == "__main__":
    unittest.main()
