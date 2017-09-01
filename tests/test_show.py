"""Show related unit tests"""

import os
import sys
import unittest

import datetime
import pytz

# Load the module locally from the dev environment.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from nowplaypadgen import show # pylint: disable=wrong-import-position


class ShowTestSuite(unittest.TestCase):
    """Show test cases."""

    def test_show_name_assignment(self):
        """Test the show name assignment"""
        show_name = "My Show Name"

        sho = show.Show(show_name)
        self.assertEqual(show_name, sho.name)


    def test_date_assignment(self):
        """Test the time setter and getter decorators"""
        sho = show.Show()

        sho.starttime = datetime.datetime(2017, 8, 30, 21, 0, 0, 0, pytz.utc)
        self.assertIsInstance(sho.starttime, datetime.datetime)

        sho.endtime = datetime.datetime(2017, 8, 30, 22, 0, 0, 0, pytz.utc)
        self.assertIsInstance(sho.endtime, datetime.datetime)


    def test_date_must_be_datetime_obj(self):
        """Test if none datetime objects will be refused"""
        sho = show.Show()

        with self.assertRaises(show.ShowError) as context_manager:
            sho.starttime = "Not a datetime.datetime object"

        self.assertEqual('starttime has to be a datetime object',
                         context_manager.exception.message)

        with self.assertRaises(show.ShowError) as context_manager:
            sho.endtime = "Not a datetime.datetime object"

        self.assertEqual('endtime has to be a datetime object',
                         context_manager.exception.message)


    def test_date_must_be_tz_aware(self):
        """Test if none TZ aware datetime objects will be refused"""
        sho = show.Show()

        with self.assertRaises(show.ShowError) as context_manager:
            sho.starttime = datetime.datetime(2017, 8, 30, 21, 0, 0, 0)

        self.assertEqual('starttime has to be a TZ aware datetime object',
                         context_manager.exception.message)

        with self.assertRaises(show.ShowError) as context_manager:
            sho.endtime = datetime.datetime(2017, 8, 30, 22, 0, 0, 0)

        self.assertEqual('endtime has to be a TZ aware datetime object',
                         context_manager.exception.message)


    def test_start_date_utc_conversion(self):
        """Test if datetime objects will be converted to UTC"""
        sho = show.Show()

        # Create localized start and end times
        zone_name = 'Europe/Zurich'
        zurich_tz = pytz.timezone(zone_name)
        start = zurich_tz.localize(datetime.datetime(2017, 8, 30, 21, 0, 0, 0))
        end = zurich_tz.localize(datetime.datetime(2017, 8, 30, 22, 0, 0, 0))
        self.assertEqual(zone_name, start.tzinfo.zone)
        self.assertEqual(zone_name, end.tzinfo.zone)

        sho.starttime = start
        sho.endtime = end

        # Start and end times must be converted to UTC internally
        self.assertEqual('UTC', sho.starttime.tzinfo.zone)
        self.assertEqual('UTC', sho.endtime.tzinfo.zone)


    def test_end_not_before_start_date(self):
        """Test that an end date can't be before a start date"""
        sho = show.Show()

        te = "hello"

        start = datetime.datetime(2017, 8, 30, 22, 0, 0, 0, pytz.utc)
        end = datetime.datetime(2017, 8, 30, 21, 0, 0, 0, pytz.utc)

        sho.starttime = start

        with self.assertRaises(show.ShowError) as context_manager:
            sho.endtime = end

        error = "endtime {0} has to be > than starttime {1}".format(end, start)
        self.assertEqual(error, context_manager.exception.message)


    def test_start_after_end_date(self):
        """Test that a start date can't be after and end date"""
        sho = show.Show()

        start = datetime.datetime(2017, 8, 30, 22, 0, 0, 0, pytz.utc)
        end = datetime.datetime(2017, 8, 30, 21, 0, 0, 0, pytz.utc)

        sho.endtime = end

        with self.assertRaises(show.ShowError) as context_manager:
            sho.starttime = start

        error = "starttime {0} has to be < than endtime {1}".format(start, end)
        self.assertEqual(error, context_manager.exception.message)



if __name__ == '__main__':
    unittest.main()
