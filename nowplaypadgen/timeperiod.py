"""A Module which helps to deal with time periods."""

import datetime

import pytz


class TimePeriodError(Exception):
    """TimePeriod related exception."""


class TimePeriod:
    """TimePeriod class which represents a period in time.

    A TimePeriod can have an absolute start and end date/time, a duration,
    it can be active, started or already ended.
    """

    def __init__(self):
        """Create class:`TimePeriod` instance."""

        self._starttime = None  #: The period's start time, initially set to None
        self._endtime = None  #: The period's end time, initially set to None
        self._duration = datetime.timedelta()  #: The period's duration,

    @property
    def starttime(self) -> datetime.datetime:
        """Get starttime.

        :return: The absolute start time of the period in UTC
        """
        return self._starttime

    @starttime.setter
    def starttime(self, starttime: datetime.datetime):
        """Setter for starttime which checks for a TZ aware datetime object.

        The setter also updates the period's duration if and endtime was
        already set.

        :param datetime.datetime starttime: The absolute start time of the
                                            period
        :raises TimePeriodError: when starttime is not a datetime object or is
                                 TZ unaware (naive)
        """

        if not isinstance(starttime, datetime.datetime):
            raise TimePeriodError("starttime has to be a datetime object")

        if starttime.tzinfo is None or starttime.tzinfo.utcoffset(starttime) is None:
            raise TimePeriodError("starttime has to be a TZ aware datetime object")

        # UTC will be used internally to simplify date and time
        # arithmetic and avoid common problems with DST boundaries.
        # See also http://pytz.sourceforge.net/
        starttime = starttime.astimezone(pytz.utc)

        if self.endtime is not None:
            if starttime > self.endtime:
                msg = "starttime {0} has to be < than endtime {1}"
                raise TimePeriodError(msg.format(starttime, self.endtime))

            self._duration = self.endtime - starttime

        self._starttime = starttime

    @property
    def endtime(self) -> datetime.datetime:
        """Getter for endtime.

        :return: The absolute end time of the period in UTC
        """
        return self._endtime

    @endtime.setter
    def endtime(self, endtime: datetime.datetime):
        """Setter for endtime which checks for a TZ aware datetime object.

        The setter also updates the period's duration if a starttime was
        already set.

        :param datetime.datetime endtime: The absolute end time of the period
        :raises TimePeriodError: when endtime is not a datetime object or
                           is TZ unaware (naive)
        """
        if not isinstance(endtime, datetime.datetime):
            raise TimePeriodError("endtime has to be a datetime object")

        if endtime.tzinfo is None or endtime.tzinfo.utcoffset(endtime) is None:
            raise TimePeriodError("endtime has to be a TZ aware datetime object")

        # UTC will be used internally to simplify date and time
        # arithmetic and avoid common problems with DST boundaries.
        # See also http://pytz.sourceforge.net/
        endtime = endtime.astimezone(pytz.utc)

        if self.starttime is not None:
            if endtime < self.starttime:
                msg = "endtime {0} has to be > than starttime {1}"
                raise TimePeriodError(msg.format(endtime, self.starttime))

            self._duration = endtime - self.starttime

        self._endtime = endtime

    @property
    def duration(self) -> datetime.timedelta:
        """Getter for duration.

        Returns the duration of a period as a :class:`datetime.timedelta`
        object.
        Note, that the duration is stored in days, seconds and microseconds in
        such an object.

        :return: The duration of the period
        """
        return self._duration

    @duration.setter
    def duration(self, duration: datetime.timedelta):
        """Set duration.

        Sets the duration of the period and calculates the start or end time if
        either one of it is defined. Note, that it is not allowed to set the
        duration if both, the start and end time, are already defined.

        :param datetime.timedelta duration: The duration of the period
        :raises TimePeriodError: if duration is not a positive
                                 :class:`timedate.timedelta` object or if start
                                 and endtime are already set (as this might
                                 change the period).
        """

        if not isinstance(duration, datetime.timedelta):
            raise TimePeriodError("duration has to be a timedelta object")

        if duration < datetime.timedelta(0):
            raise TimePeriodError("duration must be positive")

        # Prevent the start or end time from being changed once they are set
        if self.starttime is not None and self.endtime is not None:
            raise TimePeriodError("duration already defined")

        # Automatically set a missing start or end time
        if self.endtime is None and self.starttime is not None:
            self.endtime = self.starttime + duration
        elif self.starttime is None and self.endtime is not None:
            self.starttime = self.endtime - duration

        self._duration = duration

    def set_length(self, seconds: float = 0.0):
        """Set the length of a period in seconds.

        Sets the period's length in seconds, this is a helper wrapper around
        :meth:`TimePeriod.duration()`.

        :param float seconds: The length or duration of the period in seconds
        """

        self.duration = datetime.timedelta(seconds=seconds)

    def started(self) -> bool:
        """Check if the period has started.

        :return: ``True`` if the period has started, otherwise ``False``
        :rtype: bool
        """
        return (
            self._starttime is not None
            and datetime.datetime.now(pytz.utc) >= self._starttime
        )

    def ended(self) -> bool:
        """Check if the period has ended.

        :return: ``True`` if the period has ended, otherwise ``False``
        """
        return (
            self._endtime is not None
            and datetime.datetime.now(pytz.utc) >= self._endtime
        )

    def active(self) -> bool:
        """Check if the period is active.

        An active period is defined as one that has started but not ended yet.

        :return: ``True`` if the period is active, otherwise ``False``
        """
        return self.started() and not self.ended()

    def __str__(self) -> str:
        """Return a string representation of the period, useful for logging.

        >>> # pylint: disable=line-too-long
        >>> p = TimePeriod()
        >>> p.starttime = datetime.datetime(2013, 1, 1, 13, 12, 0, tzinfo=pytz.utc)
        >>> p.endtime = datetime.datetime(2113, 1, 1, 13, 12, 0, tzinfo=pytz.utc)
        >>> print(p)
        nowplaypadgen.timeperiod start: 2013-01-01 13:12:00+00:00, end: 2113-01-01 13:12:00+00:00, duration: 36524 days, 0:00:00

        :return: String containing the start time, end time and duration
        """

        # pylint: disable=line-too-long
        return f"{__name__} start: {self.starttime}, end: {self.endtime}, duration: {self.duration}"
