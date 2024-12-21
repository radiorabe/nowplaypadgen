"""Show module for broadcast shows."""

from __future__ import annotations

from typing import Self
from uuid import UUID, uuid4

from nowplaypadgen import timeperiod


class ShowError(Exception):
    """Show related exception."""


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
    >>> sh.url
    'http://pyshow.example.com'

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

    def __init__(
        self: Self,
        name: str | None = None,
        uuid: UUID | None = None,
    ) -> None:
        """Create Show instance.

        :param str name: The name of the show.
        :param uuid.UUID uuid: The UUID of the show.
        """
        self.name = name  #: The show's name
        self.uuid = uuid  #: The show's global unique identifier (UUID)
        if self.uuid is None:
            self.uuid = uuid4()
        self.description = None  #: The show's description
        self.url = None  #: The show's URL
        # Call the parent's constructor
        super().__init__()

    def __str__(self) -> str:
        """Return a string representation of the show, useful for logging.

        >>> show = Show('My Show', uuid="12345678-1234-1234-1234-123456789012")
        >>> str(show)
        "Show 'My Show' (12345678-1234-1234-1234-123456789012) start: None, end: None, url: None"

        :return: String containing the show's name, start time,
                 end time and URL.
        """  # noqa: E501
        return f"Show '{self.name}' ({self.uuid}) start: {self.starttime}, end: {self.endtime}, url: {self.url}"  # noqa: E501
