"""Show module for broadcast shows"""

import datetime
import uuid
import pytz

class ShowError(Exception):
    """Show related exception"""
    pass


class Show(object):
    """Show class which represents a specific broadcast show

       Example::

           sh = Show('My Show')

           # Optional show parameters
           sh.description = "My weekly show about Python coding"
           sh.url = 'http://pyshow.example.com

           import datetime
           import pytz

           sh.starttime = datetime.datetime(2017,8,30,21,00,00,00,pytz.utc)
           sh.endtime = datetime.datetime(2017,8,30,22,00,00,00,pytz.utc)

           if sh.active():
               "I'm on-air right now!"
    """

    def __init__(self, name=None, uid=uuid.uuid4()):
        """Constructor for the show

        :param str: The name of the show
        :param str: The UUID of the show
        """

        self.name = name #: The show's name

        self.uid = uid #: The show's global unique identifier (UUID)

        self.description = None #: The show's description

        self.url = None #: The show's URL

        self._starttime = None #: The show's start time, initially set to None

        self._endtime = None #: The show's end time, initially set to None


    @property
    def starttime(self):
        """Getter for starttime

        :return: The start time of the show in UTC
        :rtype: datetime.datetime
        """
        return self._starttime


    @starttime.setter
    def starttime(self, starttime):
        """Setter for starttime which checks for a TZ aware datetime object

        :param datetime.datetime starttime: The start time of the show
        :raises ShowError: when starttime is not a datetime object or
                           is TZ unaware (naive)
        """

        # The current TC "aware" datetime object.
        if not isinstance(starttime, datetime.datetime):
            raise ShowError("starttime has to be a datetime object")

        if starttime.tzinfo is None or starttime.tzinfo.utcoffset(starttime) is None:
            raise ShowError("starttime has to be a TZ aware datetime object")

        # UTC will be used internally to simplify date and time
        # arithmetic and avoid common problems with DST boundaries.
        # See also http://pytz.sourceforge.net/
        starttime = starttime.astimezone(pytz.utc)

        if self.endtime is not None and starttime > self.endtime:
            msg = "starttime {0} has to be < than endtime {1}"
            raise ShowError(msg.format(starttime, self.endtime))

        self._starttime = starttime


    @property
    def endtime(self):
        """Getter for endtime

        :return: The end time of the show in UTC
        :rtype: datetime.datetime
        """
        return self._endtime


    @endtime.setter
    def endtime(self, endtime):
        """Setter for endtime which checks for a TZ aware datetime object

        :param datetime.datetime endtime: The end time of the show
        :raises ShowError: when endtime is not a datetime object or
                           is TZ unaware (naive)
        """
        # The current TC "aware" datetime object.
        if not isinstance(endtime, datetime.datetime):
            raise ShowError("endtime has to be a datetime object")

        if endtime.tzinfo is None or endtime.tzinfo.utcoffset(endtime) is None:
            raise ShowError("endtime has to be a TZ aware datetime object")

        # UTC will be used internally to simplify date and time
        # arithmetic and avoid common problems with DST boundaries.
        # See also http://pytz.sourceforge.net/
        endtime = endtime.astimezone(pytz.utc)

        if self.starttime is not None and endtime < self.starttime:
            msg = "endtime {0} has to be > than starttime {1}"
            raise ShowError(msg.format(endtime, self.starttime))

        self._endtime = endtime


    def started(self):
        """Checks if the show has started

        :return: ``True`` if the show has started, otherwise ``False``
        :rtype: bool
        """
        return bool(self._starttime is not None and \
                    datetime.datetime.now(pytz.utc) >= self._starttime)


    def ended(self):
        """Checks if the show has ended

        :return: ``True`` if the show has ended, otherwise ``False``
        :rtype: bool
        """
        return bool(self._endtime is not None and \
                    datetime.datetime.now(pytz.utc) >= self._endtime)


    def active(self):
        """Checks if the show is active

        An active show is defined as one that has started but not ended yet.

        :return: ``True`` if the show is active, otherwise ``False``
        :rtype: bool
        """
        return bool(self.started() and not self.ended())


    def __str__(self):
        """Returns a string representation of the show, useful for logging

        :return: String containing the show's name, start time,
                 end time and URL
        :rtype: str
        """
        return "Show '%s' (%s), start: '%s', end: '%s', url: %s" \
                % (self.name, self.uid, self.starttime, self.endtime, self.url)
