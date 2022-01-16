"""Dynamic Label Plus (DL Plus) module.

This module offers various classes which help to deal with the DAB+ Dynamic
Label Plus (DL Plus) text feature, as defined in  `ETSI TS 102 980
<http://www.etsi.org/deliver/etsi_ts/102900_102999/102980/02.01.01_60/ts_102980v020101p.pdf>`_
(`Digital Audio Broadcasting (DAB); Dynamic Label Plus (DL Plus); Application
specification`).

A short primer about DL Plus:
A DL Plus message (:class:`DLPlusMessage`) can be
parsed into up to four DL Plus objects (:class:`DLPlusObject`) with the help of
DL Plus tags (:class:`DLPlusTag`).

Apart from that, this module also supports building a DL Plus message
(:class:`DLPlusMessage`) out of a format string an up to four DL Plus objects
(:class:`DLPlusObject`).

.. highlight:: none

Example ASCII art representation::

                    DL message (DLPlusMessage)
                   +-----------------------------------+
                   | Now playing: My Artist - My Title |
                   +-----------------------------------+
                                  |_______|   |______|
                                      V           V
                                    Artist      Title

            DL Plus tag (DLPlusTag)         DL Plus tag (DLPlusTag)
            +---------------------------+   +---------------------------+
            | Content type:  ITEM.ARTIST|   | Content type:  ITEM.TITLE |
            | Start marker:  13         |   | Start marker:  25         |
            | Length marker:  9         |   | Length marker:  8         |
            +---------------------------+   +---------------------------+
                          |                               |
                          |                               |
                          V                               V

            DL Plus object (DLPlusObject)   DL Plus tag (DLPlusObject)
            +---------------------------+   +---------------------------+
            | Content type: ITEM.ARTIST |   | Content type: ITEM.TITLE  |
            | Text:         My Artist   |   | Text:         My Title    |
            +---------------------------+   +---------------------------+
"""
from __future__ import annotations

import datetime
from typing import TypedDict

import pytz

from nowplaypadgen.util import Error

# @TODO: - Add support for item toggle and running bit
#        - Add an DL Plus object container
#        - Linking of DL Plus objects


CATEGORIES: list[str] = [
    "Dummy",
    "Item",
    "Info",
    "Programme",
    "Interactivity",
    "Private",
    "Descriptor",
]
"""Content type categories according to chapter 5.1 of ETSI TS 102 980.

    :meta hide-value:
"""


class _ContentType(TypedDict):
    """Type definition for the :attr:`CONTENT_TYPES` dictionary."""

    code: int
    category: str
    id3v1: str | None
    id3v2: str | None


CONTENT_TYPES: dict[str, _ContentType] = {
    "DUMMY": {"code": 0, "category": CATEGORIES[0], "id3v1": None, "id3v2": None},
    "ITEM.TITLE": {
        "code": 1,
        "category": CATEGORIES[1],
        "id3v1": "TITLE",
        "id3v2": "TIT2",
    },
    "ITEM.ALBUM": {
        "code": 2,
        "category": CATEGORIES[1],
        "id3v1": "ALBUM",
        "id3v2": "TALB",
    },
    "ITEM.TRACKNUMBER": {
        "code": 3,
        "category": CATEGORIES[1],
        "id3v1": "TRACKNUM",
        "id3v2": "TRCK",
    },
    "ITEM.ARTIST": {
        "code": 4,
        "category": CATEGORIES[1],
        "id3v1": "ARTIST",
        "id3v2": "TPE1",
    },
    "ITEM.COMPOSITION": {
        "code": 5,
        "category": CATEGORIES[1],
        "id3v1": "COMPOSITION",
        "id3v2": "TIT1",
    },
    "ITEM.MOVEMENT": {
        "code": 6,
        "category": CATEGORIES[1],
        "id3v1": "MOVEMENT",
        "id3v2": "TIT3",
    },
    "ITEM.CONDUCTOR": {
        "code": 7,
        "category": CATEGORIES[1],
        "id3v1": "CONDUCTOR",
        "id3v2": "TPE3",
    },
    "ITEM.COMPOSER": {
        "code": 8,
        "category": CATEGORIES[1],
        "id3v1": "COMPOSER",
        "id3v2": "TCOM",
    },
    "ITEM.BAND": {
        "code": 9,
        "category": CATEGORIES[1],
        "id3v1": "BAND",
        "id3v2": "TPE2",
    },
    "ITEM.COMMENT": {
        "code": 10,
        "category": CATEGORIES[1],
        "id3v1": "COMMENT",
        "id3v2": "COMM",
    },
    "ITEM.GENRE ": {
        "code": 11,
        "category": CATEGORIES[1],
        "id3v1": "CONTENTTYPE",
        "id3v2": "TCON",
    },
    "INFO.NEWS": {"code": 12, "category": CATEGORIES[2], "id3v1": None, "id3v2": None},
    "INFO.NEWS.LOCAL": {
        "code": 13,
        "category": CATEGORIES[2],
        "id3v1": None,
        "id3v2": None,
    },
    "INFO.STOCKMARKET": {
        "code": 14,
        "category": CATEGORIES[2],
        "id3v1": None,
        "id3v2": None,
    },
    "INFO.SPORT": {"code": 15, "category": CATEGORIES[2], "id3v1": None, "id3v2": None},
    "INFO.LOTTERY": {
        "code": 16,
        "category": CATEGORIES[2],
        "id3v1": None,
        "id3v2": None,
    },
    "INFO.HOROSCOPE": {
        "code": 17,
        "category": CATEGORIES[2],
        "id3v1": None,
        "id3v2": None,
    },
    "INFO.DAILY_DIVERSION": {
        "code": 18,
        "category": CATEGORIES[2],
        "id3v1": None,
        "id3v2": None,
    },
    "INFO.HEALTH": {
        "code": 19,
        "category": CATEGORIES[2],
        "id3v1": None,
        "id3v2": None,
    },
    "INFO.EVENT": {"code": 20, "category": CATEGORIES[2], "id3v1": None, "id3v2": None},
    "INFO.SCENE": {"code": 21, "category": CATEGORIES[2], "id3v1": None, "id3v2": None},
    "INFO.CINEMA": {
        "code": 22,
        "category": CATEGORIES[2],
        "id3v1": None,
        "id3v2": None,
    },
    "INFO.TV": {"code": 23, "category": CATEGORIES[2], "id3v1": None, "id3v2": None},
    "INFO.DATE_TIME": {
        "code": 24,
        "category": CATEGORIES[2],
        "id3v1": None,
        "id3v2": None,
    },
    "INFO.WEATHER": {
        "code": 25,
        "category": CATEGORIES[2],
        "id3v1": None,
        "id3v2": None,
    },
    "INFO.TRAFFIC": {
        "code": 26,
        "category": CATEGORIES[2],
        "id3v1": None,
        "id3v2": None,
    },
    "INFO.ALARM": {"code": 27, "category": CATEGORIES[2], "id3v1": None, "id3v2": None},
    "INFO.ADVERTISEMENT": {
        "code": 28,
        "category": CATEGORIES[2],
        "id3v1": None,
        "id3v2": None,
    },
    "INFO.URL": {"code": 29, "category": CATEGORIES[2], "id3v1": None, "id3v2": None},
    "INFO.OTHER": {"code": 30, "category": CATEGORIES[2], "id3v1": None, "id3v2": None},
    "STATIONNAME.SHORT": {
        "code": 31,
        "category": CATEGORIES[3],
        "id3v1": None,
        "id3v2": None,
    },
    "STATIONNAME.LONG": {
        "code": 32,
        "category": CATEGORIES[3],
        "id3v1": None,
        "id3v2": None,
    },
    "PROGRAMME.NOW": {
        "code": 33,
        "category": CATEGORIES[3],
        "id3v1": None,
        "id3v2": None,
    },
    "PROGRAMME.NEXT": {
        "code": 34,
        "category": CATEGORIES[3],
        "id3v1": None,
        "id3v2": None,
    },
    "PROGRAMME.PART": {
        "code": 35,
        "category": CATEGORIES[3],
        "id3v1": None,
        "id3v2": None,
    },
    "PROGRAMME.HOST": {
        "code": 36,
        "category": CATEGORIES[3],
        "id3v1": None,
        "id3v2": None,
    },
    "PROGRAMME.EDITORIAL_STAFF": {
        "code": 37,
        "category": CATEGORIES[3],
        "id3v1": None,
        "id3v2": None,
    },
    "PROGRAMME.FREQUENCY ": {
        "code": 38,
        "category": CATEGORIES[3],
        "id3v1": None,
        "id3v2": None,
    },
    "PROGRAMME.HOMEPAGE": {
        "code": 39,
        "category": CATEGORIES[3],
        "id3v1": "WWWRADIOPAGE",
        "id3v2": "WORS",
    },
    "PROGRAMME.SUBCHANNEL": {
        "code": 40,
        "category": CATEGORIES[3],
        "id3v1": None,
        "id3v2": None,
    },
    "PHONE.HOTLINE": {
        "code": 41,
        "category": CATEGORIES[4],
        "id3v1": None,
        "id3v2": None,
    },
    "PHONE.STUDIO": {
        "code": 42,
        "category": CATEGORIES[4],
        "id3v1": None,
        "id3v2": None,
    },
    "PHONE.OTHER": {
        "code": 43,
        "category": CATEGORIES[4],
        "id3v1": None,
        "id3v2": None,
    },
    "SMS.STUDIO": {"code": 44, "category": CATEGORIES[4], "id3v1": None, "id3v2": None},
    "SMS.OTHER": {"code": 45, "category": CATEGORIES[4], "id3v1": None, "id3v2": None},
    "EMAIL.HOTLINE": {
        "code": 46,
        "category": CATEGORIES[4],
        "id3v1": None,
        "id3v2": None,
    },
    "EMAIL.STUDIO": {
        "code": 47,
        "category": CATEGORIES[4],
        "id3v1": None,
        "id3v2": None,
    },
    "EMAIL.OTHER": {
        "code": 48,
        "category": CATEGORIES[4],
        "id3v1": None,
        "id3v2": None,
    },
    "MMS.OTHER": {"code": 49, "category": CATEGORIES[4], "id3v1": None, "id3v2": None},
    "CHAT": {"code": 50, "category": CATEGORIES[4], "id3v1": None, "id3v2": None},
    "CHAT.CENTER": {
        "code": 51,
        "category": CATEGORIES[4],
        "id3v1": None,
        "id3v2": None,
    },
    "VOTE.QUESTION": {
        "code": 52,
        "category": CATEGORIES[4],
        "id3v1": None,
        "id3v2": None,
    },
    "VOTE.CENTRE": {
        "code": 53,
        "category": CATEGORIES[4],
        "id3v1": None,
        "id3v2": None,
    },
    "DESCRIPTOR.PLACE": {
        "code": 59,
        "category": CATEGORIES[6],
        "id3v1": None,
        "id3v2": None,
    },
    "DESCRIPTOR.APPOINTMENT": {
        "code": 60,
        "category": CATEGORIES[6],
        "id3v1": None,
        "id3v2": None,
    },
    "DESCRIPTOR.IDENTIFIER": {
        "code": 61,
        "category": CATEGORIES[6],
        "id3v1": "ISRC",
        "id3v2": "TSRC",
    },
    "DESCRIPTOR.PURCHASE": {
        "code": 62,
        "category": CATEGORIES[6],
        "id3v1": "WWWPAYMENT",
        "id3v2": "WPAY",
    },
    "DESCRIPTOR.GET_DATA": {
        "code": 63,
        "category": CATEGORIES[6],
        "id3v1": None,
        "id3v2": None,
    },
}
"""Content types according to ETSI TS 102 980, Annex A, Table A.1.

   :meta hide-value:
"""

#: The maximum text limit in bytes according to ETSI TS 102 980, 5.0
MAXIMUM_TEXT_LIMIT = 128


class DLPlusError(Error):
    """Base exception for DL Plus."""


class DLPlusMessageError(DLPlusError):
    """DL Plus message related exceptions."""


class DLPlusContentTypeError(DLPlusError):
    """DL Plus content type related exceptions."""


class DLPlusTagError(DLPlusError):
    """DL Plus tag related exceptions."""


class DLPlusObjectError(DLPlusError):
    """DL Plus object related exceptions."""


class DLPlusMessage:
    """Dynamic Label Plus (DL Plus) message.

    This class supports parsing or building a DL Plus message string.

    If it is not initialised, it will render an empty message.

    >>> message = DLPlusMessage()
    >>> str(message)
    ''

    You can add a :class:`DLPlusObject` to the message.

    >>> message.add_dlp_object(DLPlusObject("ITEM.TITLE", "Title"))

    Render it using the :meth:`build` method.

    >>> message.build("{o[ITEM.TITLE]}")
    >>> str(message)
    'Title'

    Fetch the raw DL Plus message string.

    >>> message.message
    'Title'

    Get the detected :class:`DLPlusTag`: instances (if any).

    >>> tags = message.get_dlp_tags()
    >>> type(tags['ITEM.TITLE'])
    <class 'nowplaypadgen.dlplus.DLPlusTag'>
    """

    def __init__(self):
        """Create class:`DLPlusMessage` instance.

        Creates a new :class:`DLPlusMessage` object which can be used to parse
        or build a DL Plus message string.
        """

        #: The format string from which the message will be built
        self.format_string = ""
        #: The formatted DL Plus message
        self._message = ""
        #: Dictionary holding the assigned DL Plus objects
        self._dlp_objects = {}
        #: Dictionary holding the assigned DL Plus tags
        self._dlp_tags = {}
        #: Status if the message was successfully parsed
        self._parsed = False
        #: Status if the message was successfully built
        self._built = False

    def add_dlp_object(self, dlp_object: DLPlusObject):
        """Add a :class:`DLPlusObject` to a message string.

            This method is intended to be used before building a DL Plus Message.
            It allows one to add up to four :class:`DLPlusObject` objects which
            will replace the corresponding content type patterns (e.g.
            ``{ITEM.TITLE}``) present within the
            :attr:`DLPlusMessage.format_string`. After adding all DL Plus objects,
            :meth:`DLPlusMessage.build()` has to be called.

        :param DLPlusObject dlp_object: The DL Plus Object to add
        :raises DLPlusMessageError: when `dlp_object` is not a
                                        :class:`DLPlusObject` object, or the
                                        maximum of four :class:`DLPlusObject`
                                        objects where already added.
        """

        if not isinstance(dlp_object, DLPlusObject):
            raise DLPlusMessageError("dlp_object has to be a DLPlusObject object")

        # Up to four DL Plus objects can be created from each DL message
        # according to ETSI TS 102 980, 5.1
        if len(self._dlp_objects) >= 4:
            raise DLPlusMessageError(
                "Only a maximum of 4 DLPlusObject objects can be added"
            )

        # Use the content_type of the DL Plus object as the dictionary key
        self._dlp_objects[dlp_object.content_type] = dlp_object

    def get_dlp_objects(self) -> dict:
        """Return the associated DL Plus objects (:class:`DLPlusObject`).

        :return: Dictionary of :class:`DLPlusObject` objects.
        """
        return self._dlp_objects

    def add_dlp_tag(self, dlp_tag: DLPlusTag):
        """Add a :class:`DLPlusTag` required for parsing the message.

        This method is intended to be used before parsing a DL Plus Message.
        It allows one to add up to four :class:`DLPlusTag` objects which will
        support parsing the DL Plus message into :class:`DLPlusObject` objects.
        After adding all DL Plus tags, :meth:`DLPlusMessage.parse()` has to be
        called.

        >>> message = DLPlusMessage()
        >>> message.add_dlp_tag(DLPlusTag("ITEM.TITLE", 0, 10))

        You can add up to 4 tags.

        >>> message = DLPlusMessage()
        >>> message.add_dlp_tag(DLPlusTag("ITEM.TITLE", 0, 10))
        >>> message.add_dlp_tag(DLPlusTag("ITEM.ARTIST", 0, 10))
        >>> message.add_dlp_tag(DLPlusTag("ITEM.ALBUM", 0, 10))
        >>> message.add_dlp_tag(DLPlusTag("INFO.URL", 0, 10))
        >>> try:
        ...     message.add_dlp_tag(DLPlusTag("INFO.OTHER", 0, 10))
        ... except DLPlusMessageError as ex:
        ...     print(ex)
        Only a maximum of 4 DLPlusTag objects can be added

        :param DLPlusTag dlp_tag: The DL Plus Tag object to add
        :raises DLPlusMessageError: when `dlp_tag` is not a
                                    :class:`DLPlusTag` object, or the maximum
                                    of four :class:`DLPlusTag` objects where
                                    already added.
        """

        if not isinstance(dlp_tag, DLPlusTag):
            raise DLPlusMessageError("dlp_tag has to be a DLPlusTag object")

        # Up to four DL Plus tags can be created from each DL message
        # according to ETSI TS 102 980, 5.1
        if len(self._dlp_tags) >= 4:
            raise DLPlusMessageError(
                "Only a maximum of 4 DLPlusTag objects can be added"
            )

        self._dlp_tags[dlp_tag.content_type] = dlp_tag

    def get_dlp_tags(self) -> dict:
        """Return the associated DL Plus tags (:class:`DLPlusTag`).

        :return: Dictionary of :class:`DLPlusTag` objects.
        """
        return self._dlp_tags

    def parse(self, message: str):
        """Parse a DL Plus `message` into DL Plus objects.

        This method parses a given DL Plus `message` into zero or more DL Plus
        objects (:class:`DLPlusObject`), according to the associated DL Plus
        tags (:class:`DLPlusTag`).

        Before calling this method, one is supposed to add up to four expected
        DL Plus tags (:class:`DLPlusTag`) via the
        :meth:`DLPlusMessage.add_dlp_tag()` method.  Afterwards the newly
        created DL Plus objects (:class:`DLPlusObject`) can be retrieved via
        the :meth:`DLPlusMessage.get_dlp_objects()` method.

        >>> message = DLPlusMessage()
        >>> message.add_dlp_tag(DLPlusTag("STATIONNAME.LONG", 0, 10))
        >>> message.add_dlp_tag(DLPlusTag("STATIONNAME.SHORT", 6, 4))
        >>> message.parse("Radio RaBe")
        >>> objs = message.get_dlp_objects()
        >>> str(objs['STATIONNAME.LONG'])
        'Radio RaBe'
        >>> str(objs['STATIONNAME.SHORT'])
        'RaBe'

        If will not fail if the message is not formatted according to the DL Plus Tag

        >>> message = DLPlusMessage()
        >>> message.add_dlp_tag(DLPlusTag("STATIONNAME.LONG", 0, 10))
        >>> message.parse("RaBe")

        :param str message: The DL Plus message string which should be parsed
        """

        # Reset the DLPlusObjects
        self._dlp_objects = {}

        # Extract sub strings from the message according to the DLPlusTag
        # objects to create DLPLusObject objects
        for _, dlp_tag in self._dlp_tags.items():
            end = dlp_tag.start + dlp_tag.length

            # Delete objects have their length marker set to 0 and the start
            # marker set to a blank character, according to ETSI TS 102 980,
            # 6.2 Creating a delete object
            delete = dlp_tag.length == 0 and message[dlp_tag.start : end + 1] == " "

            self._dlp_objects[dlp_tag.content_type] = DLPlusObject(
                dlp_tag.content_type, message[dlp_tag.start : end], delete
            )

        self._message = message
        self._parsed = True

    def build(self, format_string: str):
        """Build a DL Plus message from a given format and DL Plus objects.

        This method builds a DL Plus message string from a given
        `format_string` and up to four DL Plus objects (:class:`DLPlusObject`).
        The DL Plus object's text will replace any corresponding content type
        pattern (``{o[CONTENT.TYPE]}``) within the `format_string` (with the
        help of :meth:`str.format()`). Apart from that, the required DL Plus
        tags (:class:`DLPlusTag`) will be created, with the correct `start` and
        `length` markers.

        For example, the following `format_string`
        ``Now playing: {o[ITEM.ARTIST]} - {o[ITEM.TITLE]}`` will be built into
        ``Now playing: My Artist - My Title``, given that two DL Plus objects
        (:class:`DLPlusObjects`) with the corresponding content types are
        available. Furthermore, two related DL Plus tags (:class:`DLPlusTag`)
        will be created.

        Before calling this method, one is supposed to add up to four DL Plus
        objects (:class:`DLPlusObject`) via the :meth:`DLPlusMessage.add_dlp_object()`
        method.

        >>> message = DLPlusMessage()
        >>> message.add_dlp_object(DLPlusObject("STATIONNAME.LONG", "Radio RaBe"))
        >>> message.add_dlp_object(DLPlusObject("STATIONNAME.SHORT", "RaBe"))

        You can then use the :meth:`DLPlusMessage.build()` method to build the
        DL Plus message string and create the DL Plus tags (:class:`DLPlusTag`).

        >>> message.build("{o[STATIONNAME.LONG]}")
        >>> message.message
        'Radio RaBe'

        Afterwards the newly created DL Plus tags (:class:`DLPlusTag`) can be
        retrieved via the :meth:`DLPlusMessage.get_dlp_tags()` method.

        >>> tags = message.get_dlp_tags()
        >>> long = tags['STATIONNAME.LONG']
        >>> f"{long}: {long.code} {long.start} {long.length}"
        'STATIONNAME.LONG: 32 0 10'
        >>> short = tags['STATIONNAME.SHORT']
        >>> f"{short}: {short.code} {short.start} {short.length}"
        'STATIONNAME.SHORT: 31 6 4'

        :param str format_string: The DL Plus message string format with content
                                  type replacement patterns in curly braces
                                  (such as ``{o[CONTENT.TYPE]}``).
        :raises DLPlusMessageError: if the message exceeds the maximum allowed
                                    size in bytes (:attr:`MAXIMUM_TEXT_LIMIT`).
        """
        self.format_string = format_string

        # Create the message according to the available DLPlusObjects
        # Note, that we have to use a parameter assignment
        # (o=self._dlp_objects) here, rather than directly unpack the
        # dictionary (via .format(**self._dlp_objects)). As dots in
        # keys for str.format() are not allowed and will result in KeyError
        message = self.format_string.format(o=self._dlp_objects)

        # Make sure that the byte length of the message doesn't exceed the
        # maximum allowed limit.
        if len(message.encode("utf-8")) > MAXIMUM_TEXT_LIMIT:
            raise DLPlusMessageError(
                f"Message is longer than {MAXIMUM_TEXT_LIMIT} bytes"
            )

        self._message = message

        # Reset the DLPlusTags
        self._dlp_tags = {}

        # Create DLPlusTags from the message and DLPlusObjects
        for _, dlp_object in self._dlp_objects.items():
            self._dlp_tags[dlp_object.content_type] = DLPlusTag.from_message(
                self, dlp_object.content_type
            )

        self._built = True

    @property
    def message(self) -> str:
        """Get :attr:`_message`.

        :return: Formatted DL Plus Message
        """
        return self._message

    def __str__(self) -> str:
        """Return the formatted DL Plus Message.

        :return: Formatted DL Plus Message
        """

        return self.message


class DLPlusContentType:
    """Dynamic Label Plus content type."""

    def __init__(self, content_type: str):
        """Create class:`DLPlusContentType` instance.

        Creates a new :class:`DLPlusContentType` object with a specific content
        type (`content_type`)

        For a list of supported content types see either :attr:`CONTENT_TYPES`
        or refer to `ETSI TS 102 980
        <http://www.etsi.org/deliver/etsi_ts/102900_102999/102980/02.01.01_60/ts_102980v020101p.pdf>`_,
        `Annex A (List of DL Plus content types), Table A.1`.

        :param str content_type: The content type according to ETSI TS 102 980,
                                 Annex A (List of DL Plus content types), Table
                                 A.1
        :raises DLPlusContentTypeError: if an invalid content type was specified
        """

        if content_type not in CONTENT_TYPES:
            raise DLPlusContentTypeError(f"Invalid content_type: {content_type}")

        #: The content type according to ETSI TS 102 980, Annex A, Table A.1
        self.content_type = content_type
        #: Store content_type info for later lookups
        self._content_type: _ContentType = CONTENT_TYPES[content_type]

    @property
    def code(self) -> int:
        """Get the content type code.

        Returns the content type code according to ETSI TS 102 980, Annex A
        (List of DL Plus content types), Table A.1.

        :return: The content type code
        """
        return self._content_type["code"]

    @property
    def category(self) -> str:
        """Get the content type category.

        Returns the content type category according to ETSI TS 102 980, Annex A
        (List of DL Plus content types), Table A.1.

        >>> content_type = DLPlusContentType("ITEM.ARTIST")
        >>> content_type.category
        'Item'

        :return: The content type category string
        """
        return self._content_type["category"]

    def is_dummy(self) -> bool:
        """Check whether the instance is a "dummy" object.

        Checks whether the :attr:`content_type`of the instance is set to `DUMMY`

        :return: `True` if the instance is a dummy object, otherwise `False`
        """
        return self.content_type == "DUMMY"

    def __str__(self) -> str:
        """Return the content type.

        :return: DL Plus content type
        """
        return self.content_type


class DLPlusObject(DLPlusContentType):
    """Dynamic Label Plus (DL Plus) object.

    DL Plus object which holds a text string with a defined content type.
    """

    def __init__(self, content_type: str, text: str = "", delete: bool = False):
        """Create a class:`DLPlusObject` instance.

        Creates a new :class:`DLPlusObject` object with a specific content type
        (`content_type`) and the corresponding text string (`text`).

        For a list of supported content types see either :attr:`CONTENT_TYPES`
        or refer to `ETSI TS 102 980
        <http://www.etsi.org/deliver/etsi_ts/102900_102999/102980/02.01.01_60/ts_102980v020101p.pdf>`_,
        `Annex A (List of DL Plus content types), Table A.1`.

        :param str content_type: The content type according to ETSI TS 102 980,
                                 Annex A (List of DL Plus content types), Table
                                 A.1
        :param str text: The DL Plus object text string
        :param bool delete: If `True` the object is a DL Plus Delete object
        :raises DLPlusContentTypeError: if an invalid content type was specified
        :raises DLPlusMessageError: if the text exceeds the maximum allowed size
                                    in bytes (:attr:`MAXIMUM_TEXT_LIMIT`).
        """

        # Call the parent constructor which will assign self.content_type
        super().__init__(content_type)

        # Make sure that the byte length of the text doesn't exceed the maximum
        # allowed limit.
        # https://stackoverflow.com/a/4013418/8587602
        if len(text.encode("utf-8")) > MAXIMUM_TEXT_LIMIT:
            raise DLPlusObjectError(f"Text is longer than {MAXIMUM_TEXT_LIMIT} bytes")

        # DL Plus dummy objects always have their text set to an empty string
        if self.is_dummy():
            text = ""
        # DL Plus delete objects always have their text set to a whitespace string
        if delete:
            text = " "

        #: The text string of the DL Plus object
        self.text = text

        #: Flag which specifies whether the DL Plus object is a Delete object
        self.is_delete = delete

        #: The creation time stamp of the DL Plus object in UTC
        self.creation_ts = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

        #: The expiration (deletion) time stamp of the DL Plus object in UTC
        self.expiration_ts = None

    def expire(self):
        """Set the expiration (deletion) time stamp to the current time in UTC.

        This method should be called if the current DL Plus object gets updated
        by a new one or an explicit delete object has been received. It will set
        :attr:`expiration_ts` to a TZ aware :class:`datetime.datetime` object
        representing the current time in UTC.
        """
        self.expiration_ts = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

    @classmethod
    def create_dummy(cls) -> DLPlusObject:
        """Create a dummy class:`DLPlusObject` instance.

        The factory creates a new :class:`DLPlusObject` dummy object which has
        the content type set to `DUMMY` and the text string to an empty value.

        :return: Dummy DL Plus Object
        """

        return cls("DUMMY", "")

    def __str__(self) -> str:
        """Return the DL Plus objects text.

        :return: DL Plus object text
        """
        return self.text


class DLPlusTag(DLPlusContentType):
    """Dynamic Label Plus (DL Plus) tag.

    DL plus tag which defines a start and length marker together with a content
    type.

    >>> tag = DLPlusTag(content_type="ITEM.TITLE", start=0, length=10)
    >>> print(tag)
    ITEM.TITLE

    The tag contains a start and length marker

    >>> tag.start
    0
    >>> tag.length
    10

    You can access the tags low-level DLS code point

    >>> tag.code
    1
    """

    def __init__(self, content_type: str, start: int, length: int):
        """Create a class:`DLPlusTag` instance.

        Creates a new :class:`DLPlusTag` object with a specific content type
        (`content_type`) and defined `start` and `length` markers.

        For a list of supported content types see either :attr:`CONTENT_TYPES`
        or refer to `ETSI TS 102 980
        <http://www.etsi.org/deliver/etsi_ts/102900_102999/102980/02.01.01_60/ts_102980v020101p.pdf>`_,
        `Annex A (List of DL Plus content types), Table A.1`.

        :param str content_type: The content type according to ETSI TS 102 980,
                                 Annex A (List of DL Plus content types), Table
                                 A.1
        :param int start: Start marker of a DL Plus object (the start index of
                          the DL Plus object's text)
        :param int length: Length marker of a DL Plus object (the string length
                           of the DL Plus object's text)
        :raises DLPlusContentTypeError: if an invalid content type was specified
        :raises DLPlusTagError: if either `start` or `length` are not a positive
                                integer.
        """

        # Call the parent constructor which will assign self.content_type
        super().__init__(content_type)

        if not isinstance(start, int) or start < 0:
            raise DLPlusTagError("start must be a positive integer")

        if not isinstance(length, int) or length < 0:
            raise DLPlusTagError("length must be a positive integer")

        # Dummy objects always have their start and length marker set to 0
        if self.is_dummy():
            start = 0
            length = 0

        self.start = start
        self.length = length

    @classmethod
    def from_message(cls, dlp_message: DLPlusMessage, content_type: str) -> DLPlusTag:
        """Create a class:`DLPlusTag` instance from a :class:`DLPlusMessage`.

        The factory creates a new :class:`DLPlusTag` object from an existing
        and already populated :class:`DLPlusMessage` object, this way one
        doesn't has to calculate and specify the `start` and `length` markers.

        >>> message = DLPlusMessage()
        >>> message.add_dlp_object(DLPlusObject("STATIONNAME.LONG", "Radio RaBe"))
        >>> message.add_dlp_object(DLPlusObject("STATIONNAME.SHORT", "RaBe"))
        >>> message.build("{o[STATIONNAME.LONG]}")
        >>> tag = DLPlusTag.from_message(message, "STATIONNAME.SHORT")
        >>> f"{tag.content_type} {tag.start} {tag.length}"
        'STATIONNAME.SHORT 6 4'

        It also handles delete tags in messages

        >>> message = DLPlusMessage()
        >>> message.add_dlp_object(DLPlusObject("ITEM.TITLE", delete=True))
        >>> message.build("I am string")
        >>> tag = DLPlusTag.from_message(message, "ITEM.TITLE")
        >>> f"{tag.content_type} {tag.start} {tag.length}"
        'ITEM.TITLE 1 0'

        :param DLPlusMessage dlp_message: The populated DL Plus message
        :return: DL Plus Tag
        """

        # Pythonic factory class method according to:
        # * https://stackoverflow.com/a/14992545
        # * https://stackoverflow.com/a/12179752

        if not isinstance(dlp_message, DLPlusMessage):
            raise DLPlusTagError("dlp_message has to be a DLPlusMessage")

        if content_type not in CONTENT_TYPES:
            raise DLPlusContentTypeError(f"Invalid content_type: {content_type}")

        # Check that a DLPlusObject object for the requested content type
        # was added and is available.
        try:
            dlp_object = dlp_message.get_dlp_objects()[content_type]
        except KeyError as key_error:
            raise DLPlusTagError(
                f"No DLPlusObject for content type {content_type} available"
            ) from key_error

        # Get the start marker (index) of the DL Plus object's text
        start = dlp_message.message.find(dlp_object.text)

        # Get the string length of the DL Plus object's text
        length = len(dlp_object.text)
        if dlp_object.is_delete:
            length = 0

        return cls(content_type, start, length)

    @classmethod
    def create_dummy(cls) -> DLPlusTag:
        """Create a dummy instance of class:`DLPlusTag`.

        This factory creates a :class:`DLPlusTag` dummy instance which has
        the content type set to `DUMMY` and the start and length marker set to
        0 (zero).

        :return: Dummy DL Plus Tag
        """

        return cls("DUMMY", 0, 0)
