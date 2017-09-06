"""Show module for broadcast shows"""

import uuid

from nowplaypadgen import timeperiod


class ShowError(Exception):
    """Show related exception"""
    pass


class Show(timeperiod.TimePeriod):
    """Show class which represents a specific broadcast show.

    A show has a name, a unique identifier, an optional description and URL,
    as well as an absolute start and end date/time. A show can be active,
    started or ended.

    The show constructor expects a single string with the name of the show.

    >>> sh = Show('My Show')

    You can set optional attributes on shows.

    >>> sh.description = "My weekly show about Python coding"
    >>> sh.url = 'http://pyshow.example.com'

    In this example we set our hour long show to have finished an hour ago.

    >>> import pytz
    >>> from datetime import datetime, timedelta
    >>>
    >>> sh.starttime = datetime.now(tz=pytz.utc) - timedelta(hours=2)
    >>> sh.endtime = datetime.now(tz=pytz.utc) - timedelta(hours=1)
    >>>
    >>> sh.active()
    False

    Now we change the end time so that the show ends in an hour.

    >>> sh.endtime = datetime.now(tz=pytz.utc) + timedelta(hours=1)
    >>>
    >>> sh.active()
    True
    """

    def __init__(self, name=None, uid=uuid.uuid4()):
        # type: (str, uuid.UUID) -> None
        """Constructor for the show

        :param str name: The name of the show.
        :param uuid.UUID uid: The UUID of the show.
        """

        self.name = name  # : The show's name

        self.uid = uid  # : The show's global unique identifier (UUID)

        self.description = None  # : The show's description

        self.url = None # : The show's URL

        # Call the parent's constructor
        super(Show, self).__init__()

    def __str__(self):
        """Return a string representation of the show, useful for logging.

        :return: String containing the show's name, start time,
                 end time and URL.
        :rtype: str
        """
        return ("Show '%(name)' (%(uid)), "
                "start: '%(startime)', "
                "end: '%(endtime)', "
                "url: '%(url)'"
               ).format(name=self.name,
                        uid=self.uid,
                        starttime=self.starttime,
                        endtime=self.endtime,
                        url=self.url)
