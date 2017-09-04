"""TimePeriod related unit tests"""

import os
import sys
import unittest

import datetime
import pytz

# Load the module locally from the dev environment.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from nowplaypadgen import timeperiod # pylint: disable=wrong-import-position


class TimePeriodTestSuite(unittest.TestCase):
    """TimePeriod test cases."""

    def setUp(self):
        self.period = timeperiod.TimePeriod()

    def test_date_assignment(self):
        """Test the time setter and getter decorators"""

        self.period.starttime = datetime.datetime(
            2017, 8, 30, 21, 0, 0, 0, pytz.utc)

        self.assertIsInstance(self.period.starttime, datetime.datetime)

        self.period.endtime = datetime.datetime(
            2017, 8, 30, 22, 0, 0, 0, pytz.utc)

        self.assertIsInstance(self.period.endtime, datetime.datetime)


    def test_date_must_be_datetime_obj(self):
        """Test if none datetime objects will be refused"""

        with self.assertRaises(timeperiod.TimePeriodError) as context_manager:
            self.period.starttime = "Not a datetime.datetime object"

        self.assertEqual('starttime has to be a datetime object',
                         str(context_manager.exception))

        with self.assertRaises(timeperiod.TimePeriodError) as context_manager:
            self.period.endtime = "Not a datetime.datetime object"

        self.assertEqual('endtime has to be a datetime object',
                         str(context_manager.exception))


    def test_date_must_be_tz_aware(self):
        """Test if none TZ aware datetime objects will be refused"""

        with self.assertRaises(timeperiod.TimePeriodError) as context_manager:
            self.period.starttime = datetime.datetime(2017, 8, 30, 21, 0, 0, 0)

        self.assertEqual('starttime has to be a TZ aware datetime object',
                         str(context_manager.exception))

        with self.assertRaises(timeperiod.TimePeriodError) as context_manager:
            self.period.endtime = datetime.datetime(2017, 8, 30, 22, 0, 0, 0)

        self.assertEqual('endtime has to be a TZ aware datetime object',
                         str(context_manager.exception))


    def test_start_date_utc_conversion(self):
        """Test if datetime objects will be converted to UTC"""

        # Create localized start and end times
        zone_name = 'Europe/Zurich'
        zurich_tz = pytz.timezone(zone_name)
        start = zurich_tz.localize(datetime.datetime(2017, 8, 30, 21, 0, 0, 0))
        end = zurich_tz.localize(datetime.datetime(2017, 8, 30, 22, 0, 0, 0))
        self.assertEqual(zone_name, start.tzinfo.zone)
        self.assertEqual(zone_name, end.tzinfo.zone)

        self.period.starttime = start
        self.period.endtime = end

        # Start and end times must be converted to UTC internally
        self.assertEqual('UTC', self.period.starttime.tzinfo.zone)
        self.assertEqual('UTC', self.period.endtime.tzinfo.zone)


    def test_end_not_before_start_date(self):
        """Test that an end date can't be before a start date"""

        start = datetime.datetime(2017, 8, 30, 22, 0, 0, 0, pytz.utc)
        end = datetime.datetime(2017, 8, 30, 21, 0, 0, 0, pytz.utc)

        self.period.starttime = start

        with self.assertRaises(timeperiod.TimePeriodError) as context_manager:
            self.period.endtime = end

        error = "endtime {0} has to be > than starttime {1}".format(end, start)
        self.assertEqual(error, str(context_manager.exception))


    def test_start_after_end_date(self):
        """Test that a start date can't be after and end date"""


        start = datetime.datetime(2017, 8, 30, 22, 0, 0, 0, pytz.utc)
        end = datetime.datetime(2017, 8, 30, 21, 0, 0, 0, pytz.utc)

        self.period.endtime = end

        with self.assertRaises(timeperiod.TimePeriodError) as context_manager:
            self.period.starttime = start

        error = "starttime {0} has to be < than endtime {1}".format(start, end)
        self.assertEqual(error, str(context_manager.exception))


    def test_period_has_started(self):
        """Test that a period has started"""

        now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

        self.period.starttime = now
        self.period.endtime = now + datetime.timedelta(hours=1) # plus one hour

        self.assertTrue(self.period.active())
        self.assertTrue(self.period.started())
        self.assertFalse(self.period.ended())


    def test_period_has_not_started(self):
        """Test that a period hasn't started yet"""

        now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

        self.period.starttime = now + datetime.timedelta(hours=1) # plus one hour
        self.period.endtime = now + datetime.timedelta(hours=2) # plus two hours
        self.assertFalse(self.period.active())
        self.assertFalse(self.period.started())
        self.assertFalse(self.period.ended())


    def test_period_has_ended(self):
        """Test that a period has ended"""

        now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

        self.period.starttime = now - datetime.timedelta(hours=2) # minus two hours
        self.period.endtime = now - datetime.timedelta(hours=1) # minus one hour
        self.assertFalse(self.period.active())
        self.assertTrue(self.period.started())
        self.assertTrue(self.period.ended())


    def test_period_has_not_ended(self):
        """Test that a period hasn't ended yet"""

        now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

        self.period.starttime = now
        self.period.endtime = now + datetime.timedelta(hours=1) # plus one hour
        self.assertTrue(self.period.active())
        self.assertTrue(self.period.started())
        self.assertFalse(self.period.ended())


    def test_get_period_duration(self):
        """Test get duration (time delta) of a period"""

        now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

        # The period spans one hour
        self.period.starttime = now
        self.period.endtime = now + datetime.timedelta(hours=1)

        expected_delta = datetime.timedelta(0, 3600)

        self.assertEqual(self.period.duration, expected_delta)


    def test_set_period_duration(self):
        """Test set duration (time delta) of a period"""

        duration = datetime.timedelta(hours=1)
        self.period.duration = duration

        self.assertEqual(self.period.duration, duration)


    def test_duration_must_be_timedelta(self):
        """Test if none timedelta period objects will be refused"""

        with self.assertRaises(timeperiod.TimePeriodError) as context_manager:
            self.period.duration = "Not a datetime.timedelta object"

        self.assertEqual('duration has to be a timedelta object',
                         str(context_manager.exception))


    def test_duration_must_be_positive(self):
        """Test that only positive durations will be accepted"""
        with self.assertRaises(timeperiod.TimePeriodError) as context_manager:
            self.period.duration = datetime.timedelta(seconds=-1)

        self.assertEqual('duration must be positive',
                         str(context_manager.exception))


    def test_duration_already_defined(self):
        """Test that a duration can't be changed"""

        now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

        # This should automatically set the duration, as a start and end time is
        # known by the period
        self.period.starttime = now
        self.period.endtime = now + datetime.timedelta(hours=1)

        with self.assertRaises(timeperiod.TimePeriodError) as context_manager:
            self.period.duration = datetime.timedelta(hours=2)

        self.assertEqual('duration already defined',
                         str(context_manager.exception))


    def test_duration_sets_endtime(self):
        """Test that a duration will set a currently unknown end time"""

        now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        duration = datetime.timedelta(hours=1)

        self.period.starttime = now
        self.period.duration = duration

        self.assertEqual(self.period.endtime, now + duration)


    def test_duration_sets_starttime(self):
        """Test that a duration will set a currently unknown start time"""

        now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        duration = datetime.timedelta(hours=1)

        self.period.endtime = now
        self.period.duration = duration

        self.assertEqual(self.period.starttime, now - duration)


    def test_set_length(self):
        """Test that the duration can be set using seconds"""

        duration = datetime.timedelta(hours=1)
        self.period.set_length(3600)

        self.assertEqual(self.period.duration, duration)

if __name__ == '__main__':
    unittest.main()
