import os
import sys
import unittest

import datetime
import pytz

# Load the module locally from the dev environment.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from nowplaypadgen import show


class ShowTestSuite(unittest.TestCase):
    """Show test cases."""

    def test_show_name_assignment(self):
        """Test the show name assignment"""
        show_name="My Show Name"

        s = show.Show(show_name)
        self.assertEqual(show_name, s.name)


    def test_date_assignment(self):
        """Test the time setter and getter decorators"""
        s = show.Show()

        s.starttime = datetime.datetime(2017,8,30,21,0,0,0,pytz.utc)
        self.assertIsInstance(s.starttime, datetime.datetime)

        s.endtime = datetime.datetime(2017,8,30,22,0,0,0,pytz.utc)
        self.assertIsInstance(s.endtime, datetime.datetime)


    def test_date_must_be_datetime_object(self):
        """Test if none datetime objects will be refused"""
        s = show.Show()

        with self.assertRaises(show.ShowError) as cm:
            s.starttime = "Not a datetime.datetime object"

        self.assertEqual('starttime has to be a datetime object',
                        str(cm.exception))

        with self.assertRaises(show.ShowError) as cm:
            s.endtime = "Not a datetime.datetime object"

        self.assertEqual('endtime has to be a datetime object',
                        str(cm.exception))


    def test_date_must_be_timezone_aware(self):
        """Test if none TZ aware datetime objects will be refused"""
        s = show.Show()

        with self.assertRaises(show.ShowError) as cm:
            s.starttime = datetime.datetime(2017,8,30,21,0,0,0)

        self.assertEqual('starttime has to be a TZ aware datetime object',
                        str(cm.exception))

        with self.assertRaises(show.ShowError) as cm:
            s.endtime = datetime.datetime(2017,8,30,22,0,0,0)

        self.assertEqual('endtime has to be a TZ aware datetime object',
                        str(cm.exception))


    def test_start_date_utc_conversion(self):
        """Test if datetime objects will be converted to UTC"""
        s = show.Show()

        # Create localized start and end times
        zone_name = 'Europe/Zurich'
        tz = pytz.timezone(zone_name)
        st = tz.localize(datetime.datetime(2017,8,30,21,0,0,0))
        et = tz.localize(datetime.datetime(2017,8,30,22,0,0,0))
        self.assertEqual(zone_name, st.tzinfo.zone)
        self.assertEqual(zone_name, et.tzinfo.zone)

        s.starttime = st
        s.endtime = et

        # Start and end times must be converted to UTC internally
        self.assertEqual('UTC', s.starttime.tzinfo.zone)
        self.assertEqual('UTC', s.endtime.tzinfo.zone)


    def test_end_date_not_before_start_date(self):
        """Test that an end date can't be before a start date"""
        s = show.Show()

        st = datetime.datetime(2017,8,30,22,0,0,0,pytz.utc)
        et = datetime.datetime(2017,8,30,21,0,0,0,pytz.utc)

        s.starttime = st

        with self.assertRaises(show.ShowError) as cm:
            s.endtime = et

        e = "endtime {0} has to be > than starttime {1}".format(et, st)
        self.assertEqual(e, str(cm.exception))


    def test_start_date_after_end_date(self):
        """Test that a start date can't be after and end date"""
        s = show.Show()

        st = datetime.datetime(2017,8,30,22,0,0,0,pytz.utc)
        et = datetime.datetime(2017,8,30,21,0,0,0,pytz.utc)

        s.endtime = et

        with self.assertRaises(show.ShowError) as cm:
            s.starttime = st

        e = "starttime {0} has to be < than endtime {1}".format(st, et)
        self.assertEqual(e, str(cm.exception))



if __name__ == '__main__':
    unittest.main()
