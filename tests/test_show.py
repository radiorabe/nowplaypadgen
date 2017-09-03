"""Tests for show related classes"""

import unittest
import datetime

import pytz

from nowplaypadgen import show

class ShowTestSuite(unittest.TestCase):
    """Show test cases."""

    def test_show_name_assignment(self):
        """Test the show name assignment"""
        show_name = "My Show Name"

        my_show = show.Show(show_name)
        self.assertEqual(show_name, my_show.name)

    def test_date_assignment(self):
        """Test the time setter and getter decorators"""
        my_show = show.Show()

        my_show.starttime = datetime.datetime(2017, 8, 30, 21, 0, 0, 0, pytz.utc)
        self.assertIsInstance(my_show.starttime, datetime.datetime)

        my_show.endtime = datetime.datetime(2017, 8, 30, 22, 0, 0, 0, pytz.utc)
        self.assertIsInstance(my_show.endtime, datetime.datetime)

    def test_is_date_datetime_object(self):
        """Test if none datetime objects will be refused"""
        my_show = show.Show()

        with self.assertRaises(show.ShowError) as my_show_error:
            my_show.starttime = "Not a datetime.datetime object"

        self.assertEqual('starttime has to be a datetime object',
                         str(my_show_error.exception))

        with self.assertRaises(show.ShowError) as my_show_error:
            my_show.endtime = "Not a datetime.datetime object"

        self.assertEqual('endtime has to be a datetime object',
                         str(my_show_error.exception))

    def test_is_date_timezone_aware(self):
        """Test if none TZ aware datetime objects will be refused"""
        my_show = show.Show()

        with self.assertRaises(show.ShowError) as my_show_error:
            my_show.starttime = datetime.datetime(2017, 8, 30, 21, 0, 0, 0)

        self.assertEqual('starttime has to be a TZ aware datetime object',
                         str(my_show_error.exception))

        with self.assertRaises(show.ShowError) as my_show_error:
            my_show.endtime = datetime.datetime(2017, 8, 30, 22, 0, 0, 0)

        self.assertEqual('endtime has to be a TZ aware datetime object',
                         str(my_show_error.exception))

    def test_start_date_utc_conversion(self):
        """Test if datetime objects will be converted to UTC"""
        my_show = show.Show()

        # Create localized start and end times
        zone_name = 'Europe/Zurich'
        time_zone = pytz.timezone(zone_name)
        start_date = time_zone.localize(datetime.datetime(2017, 8, 30, 21, 0, 0, 0))
        end_date = time_zone.localize(datetime.datetime(2017, 8, 30, 22, 0, 0, 0))
        self.assertEqual(zone_name, start_date.tzinfo.zone)
        self.assertEqual(zone_name, end_date.tzinfo.zone)

        my_show.starttime = start_date
        my_show.endtime = end_date

        # Start and end times must be converted to UTC internally
        self.assertEqual('UTC', my_show.starttime.tzinfo.zone)
        self.assertEqual('UTC', my_show.endtime.tzinfo.zone)

    def test_start_date_before_end_date(self):
        """Test that an end date can't be before a start date"""
        my_show = show.Show()

        start_date = datetime.datetime(2017, 8, 30, 22, 0, 0, 0, pytz.utc)
        end_date = datetime.datetime(2017, 8, 30, 21, 0, 0, 0, pytz.utc)

        my_show.starttime = start_date

        with self.assertRaises(show.ShowError) as my_show_error:
            my_show.endtime = end_date

        error = "endtime {0} has to be > than starttime {1}".format(end_date, start_date)
        self.assertEqual(error, str(my_show_error.exception))

    def test_start_date_after_end_date(self):
        """Test that a start date can't be after and end date"""
        my_show = show.Show()

        start_date = datetime.datetime(2017, 8, 30, 22, 0, 0, 0, pytz.utc)
        end_date = datetime.datetime(2017, 8, 30, 21, 0, 0, 0, pytz.utc)

        my_show.endtime = end_date

        with self.assertRaises(show.ShowError) as my_show_error:
            my_show.starttime = start_date

        error = "starttime {0} has to be < than endtime {1}".format(start_date, end_date)
        self.assertEqual(error, str(my_show_error.exception))



if __name__ == '__main__':
    unittest.main()
