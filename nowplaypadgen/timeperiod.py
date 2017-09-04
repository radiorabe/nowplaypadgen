"""A Module which helps to deal with time periods"""

import datetime
import pytz

class TimePeriodError(Exception):
    """TimePeriod related exception"""
    pass


class TimePeriod(object):
    """TimePeriod class which represents a period in time

       A TimePeriod has an absolute start and end date/time, it can be active,
       started or already ended.
    """

    def __init__(self):
        """Constructor for the time period"""

        self._starttime = None #: The period's start time, initially set to None

        self._endtime = None #: The period's end time, initially set to None


    @property
    def starttime(self):
        """Getter for starttime

        :return: The absolute start time of the period in UTC
        :rtype: datetime.datetime
        """
        return self._starttime


    @starttime.setter
    def starttime(self, starttime):
        """Setter for starttime which checks for a TZ aware datetime object

        :param datetime.datetime starttime: The absolute start time of the
                                            period
        :raises TimePeriodError: when starttime is not a datetime object or is
                                 TZ unaware (naive)
        """

        # The current TC "aware" datetime object.
        if not isinstance(starttime, datetime.datetime):
            raise TimePeriodError("starttime has to be a datetime object")

        if starttime.tzinfo is None or starttime.tzinfo.utcoffset(starttime) is None:
            raise TimePeriodError("starttime has to be a TZ aware datetime object")

        # UTC will be used internally to simplify date and time
        # arithmetic and avoid common problems with DST boundaries.
        # See also http://pytz.sourceforge.net/
        starttime = starttime.astimezone(pytz.utc)

        if self.endtime is not None and starttime > self.endtime:
            msg = "starttime {0} has to be < than endtime {1}"
            raise TimePeriodError(msg.format(starttime, self.endtime))

        self._starttime = starttime


    @property
    def endtime(self):
        """Getter for endtime

        :return: The absolute end time of the period in UTC
        :rtype: datetime.datetime
        """
        return self._endtime


    @endtime.setter
    def endtime(self, endtime):
        """Setter for endtime which checks for a TZ aware datetime object

        :param datetime.datetime endtime: The absolute end time of the period
        :raises TimePeriodError: when endtime is not a datetime object or
                           is TZ unaware (naive)
        """
        # The current TC "aware" datetime object.
        if not isinstance(endtime, datetime.datetime):
            raise TimePeriodError("endtime has to be a datetime object")

        if endtime.tzinfo is None or endtime.tzinfo.utcoffset(endtime) is None:
            raise TimePeriodError("endtime has to be a TZ aware datetime object")

        # UTC will be used internally to simplify date and time
        # arithmetic and avoid common problems with DST boundaries.
        # See also http://pytz.sourceforge.net/
        endtime = endtime.astimezone(pytz.utc)

        if self.starttime is not None and endtime < self.starttime:
            msg = "endtime {0} has to be > than starttime {1}"
            raise TimePeriodError(msg.format(endtime, self.starttime))

        self._endtime = endtime


    def started(self):
        """Checks if the period has started

        :return: ``True`` if the period has started, otherwise ``False``
        :rtype: bool
        """
        return bool(self._starttime is not None and \
                    datetime.datetime.now(pytz.utc) >= self._starttime)


    def ended(self):
        """Checks if the period has ended

        :return: ``True`` if the period has ended, otherwise ``False``
        :rtype: bool
        """
        return bool(self._endtime is not None and \
                    datetime.datetime.now(pytz.utc) >= self._endtime)


    def active(self):
        """Checks if the period is active

        An active period is defined as one that has started but not ended yet.

        :return: ``True`` if the period is active, otherwise ``False``
        :rtype: bool
        """
        return bool(self.started() and not self.ended())


    def get_duration(self):
        """Get the duration (time delta) of a period

        Returns the duration of a period as a :class:datetime.timedelta object.
        Note, that the duration is stored in days, seconds and microseconds in
        such an object.

        :return: The duration (time delta) of the period
        :rtype: datetime.timedelta
        """
        return self.endtime - self.starttime


    def __str__(self):
        """Returns a string representation of the period, useful for logging

        :return: String containing the start time, end time and duration
        :rtype: str
        """
        return '{1} start: {2}, end: {3}, duration: {4}'.format(
            __name__, self.starttime, self.endtime, self.get_duration())
