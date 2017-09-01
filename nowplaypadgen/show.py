"""Show module for broadcast shows"""

import uuid
import timeperiod

class ShowError(Exception):
    """Show related exception"""
    pass


class Show(timeperiod.TimePeriod):
    """Show class which represents a specific broadcast show

       A show has a name, a unique identifier, an optional description and URL,
       as well as an absolute start and end date/time. A show can be active,
       started or ended.

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

        # Call the parent's constructor
        super(Show, self).__init__()


    def __str__(self):
        """Returns a string representation of the show, useful for logging

        :return: String containing the show's name, start time,
                 end time and URL
        :rtype: str
        """
        return "Show '%s' (%s), start: '%s', end: '%s', url: %s" \
                % (self.name, self.uid, self.starttime, self.endtime, self.url)
