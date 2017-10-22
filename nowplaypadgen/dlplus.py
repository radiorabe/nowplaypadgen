"""Dynamic Label Plus (DL Plus) module

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

import datetime
import pytz
from future.utils import python_2_unicode_compatible

# @TODO: - Add support for item toggle and running bit
#        - Add an DL Plus object container
#        - Linking of DL Plus objects

#: Content type categories according to chapter 5.1 of ETSI TS 102 980
CATEGORIES = ['Dummy', 'Item', 'Info', 'Programme',
              'Interactivity', 'Private', 'Descriptor']

#: Content types according to ETSI TS 102 980, Annex A, Table A.1
CONTENT_TYPES = {
    'DUMMY': {
        'code': 0,
        'category': CATEGORIES[0],
        'id3v1': None,
        'id3v2': None
    },
    'ITEM.TITLE': {
        'code': 1,
        'category': CATEGORIES[1],
        'id3v1': 'TITLE',
        'id3v2': 'TIT2'
    },
    'ITEM.ALBUM': {
        'code': 2,
        'category': CATEGORIES[1],
        'id3v1': 'ALBUM',
        'id3v2': 'TALB'
    },
    'ITEM.TRACKNUMBER': {
        'code': 3,
        'category': CATEGORIES[1],
        'id3v1': 'TRACKNUM',
        'id3v2': 'TRCK'
    },
    'ITEM.ARTIST': {
        'code': 4,
        'category': CATEGORIES[1],
        'id3v1': 'ARTIST',
        'id3v2': 'TPE1'
    },
    'ITEM.COMPOSITION': {
        'code': 5,
        'category': CATEGORIES[1],
        'id3v1': 'COMPOSITION',
        'id3v2': 'TIT1'
    },
    'ITEM.MOVEMENT': {
        'code': 6,
        'category': CATEGORIES[1],
        'id3v1': 'MOVEMENT',
        'id3v2': 'TIT3'
    },
    'ITEM.CONDUCTOR': {
        'code': 7,
        'category': CATEGORIES[1],
        'id3v1': 'CONDUCTOR',
        'id3v2': 'TPE3'
    },
    'ITEM.COMPOSER': {
        'code': 8,
        'category': CATEGORIES[1],
        'id3v1': 'COMPOSER',
        'id3v2': 'TCOM'
    },
    'ITEM.BAND': {
        'code': 9,
        'category': CATEGORIES[1],
        'id3v1': 'BAND',
        'id3v2': 'TPE2'
    },
    'ITEM.COMMENT': {
        'code': 10,
        'category': CATEGORIES[1],
        'id3v1': 'COMMENT',
        'id3v2': 'COMM'
    },
    'ITEM.GENRE ': {
        'code': 11,
        'category': CATEGORIES[1],
        'id3v1': 'CONTENTTYPE',
        'id3v2': 'TCON'
    },
    'INFO.NEWS': {
        'code': 12,
        'category': CATEGORIES[2],
        'id3v1': None,
        'id3v2': None
    },
    'INFO.NEWS.LOCAL': {
        'code': 13,
        'category': CATEGORIES[2],
        'id3v1': None,
        'id3v2': None
    },
    'INFO.STOCKMARKET': {
        'code': 14,
        'category': CATEGORIES[2],
        'id3v1': None,
        'id3v2': None
    },
    'INFO.SPORT': {
        'code': 15,
        'category': CATEGORIES[2],
        'id3v1': None,
        'id3v2': None
    },
    'INFO.LOTTERY': {
        'code': 16,
        'category': CATEGORIES[2],
        'id3v1': None,
        'id3v2': None
    },
    'INFO.HOROSCOPE': {
        'code': 17,
        'category': CATEGORIES[2],
        'id3v1': None,
        'id3v2': None
    },
    'INFO.DAILY_DIVERSION': {
        'code': 18,
        'category': CATEGORIES[2],
        'id3v1': None,
        'id3v2': None
    },
    'INFO.HEALTH': {
        'code': 19,
        'category': CATEGORIES[2],
        'id3v1': None,
        'id3v2': None
    },
    'INFO.EVENT': {
        'code': 20,
        'category': CATEGORIES[2],
        'id3v1': None,
        'id3v2': None
    },
    'INFO.SCENE': {
        'code': 21,
        'category': CATEGORIES[2],
        'id3v1': None,
        'id3v2': None
    },
    'INFO.CINEMA': {
        'code': 22,
        'category': CATEGORIES[2],
        'id3v1': None,
        'id3v2': None
    },
    'INFO.TV': {
        'code': 23,
        'category': CATEGORIES[2],
        'id3v1': None,
        'id3v2': None
    },
    'INFO.DATE_TIME': {
        'code': 24,
        'category': CATEGORIES[2],
        'id3v1': None,
        'id3v2': None
    },
    'INFO.WEATHER': {
        'code': 25,
        'category': CATEGORIES[2],
        'id3v1': None,
        'id3v2': None
    },
    'INFO.TRAFFIC': {
        'code': 26,
        'category': CATEGORIES[2],
        'id3v1': None,
        'id3v2': None
    },
    'INFO.ALARM': {
        'code': 27,
        'category': CATEGORIES[2],
        'id3v1': None,
        'id3v2': None
    },
    'INFO.ADVERTISEMENT': {
        'code': 28,
        'category': CATEGORIES[2],
        'id3v1': None,
        'id3v2': None
    },
    'INFO.URL': {
        'code': 29,
        'category': CATEGORIES[2],
        'id3v1': None,
        'id3v2': None
    },
    'INFO.OTHER': {
        'code': 30,
        'category': CATEGORIES[2],
        'id3v1': None,
        'id3v2': None
    },
    'STATIONNAME.SHORT': {
        'code': 31,
        'category': CATEGORIES[3],
        'id3v1': None,
        'id3v2': None
    },
    'STATIONNAME.LONG': {
        'code': 32,
        'category': CATEGORIES[3],
        'id3v1': None,
        'id3v2': None
    },
    'PROGRAMME.NOW': {
        'code': 33,
        'category': CATEGORIES[3],
        'id3v1': None,
        'id3v2': None
    },
    'PROGRAMME.NEXT': {
        'code': 34,
        'category': CATEGORIES[3],
        'id3v1': None,
        'id3v2': None
    },
    'PROGRAMME.PART': {
        'code': 35,
        'category': CATEGORIES[3],
        'id3v1': None,
        'id3v2': None
    },
    'PROGRAMME.HOST': {
        'code': 36,
        'category': CATEGORIES[3],
        'id3v1': None,
        'id3v2': None
    },
    'PROGRAMME.EDITORIAL_STAFF': {
        'code': 37,
        'category': CATEGORIES[3],
        'id3v1': None,
        'id3v2': None
    },
    'PROGRAMME.FREQUENCY ': {
        'code': 38,
        'category': CATEGORIES[3],
        'id3v1': None,
        'id3v2': None
    },
    'PROGRAMME.HOMEPAGE': {
        'code': 39,
        'category': CATEGORIES[3],
        'id3v1': 'WWWRADIOPAGE',
        'id3v2': 'WORS'
    },
    'PROGRAMME.SUBCHANNEL': {
        'code': 40,
        'category': CATEGORIES[3],
        'id3v1': None,
        'id3v2': None
    },
    'PHONE.HOTLINE': {
        'code': 41,
        'category': CATEGORIES[4],
        'id3v1': None,
        'id3v2': None
    },
    'PHONE.STUDIO': {
        'code': 42,
        'category': CATEGORIES[4],
        'id3v1': None,
        'id3v2': None
    },
    'PHONE.OTHER': {
        'code': 43,
        'category': CATEGORIES[4],
        'id3v1': None,
        'id3v2': None
    },
    'SMS.STUDIO': {
        'code': 44,
        'category': CATEGORIES[4],
        'id3v1': None,
        'id3v2': None
    },
    'SMS.OTHER': {
        'code': 45,
        'category': CATEGORIES[4],
        'id3v1': None,
        'id3v2': None
    },
    'EMAIL.HOTLINE': {
        'code': 46,
        'category': CATEGORIES[4],
        'id3v1': None,
        'id3v2': None
    },
    'EMAIL.STUDIO': {
        'code': 47,
        'category': CATEGORIES[4],
        'id3v1': None,
        'id3v2': None
    },
    'EMAIL.OTHER': {
        'code': 48,
        'category': CATEGORIES[4],
        'id3v1': None,
        'id3v2': None
    },
    'MMS.OTHER': {
        'code': 49,
        'category': CATEGORIES[4],
        'id3v1': None,
        'id3v2': None
    },
    'CHAT': {
        'code': 50,
        'category': CATEGORIES[4],
        'id3v1': None,
        'id3v2': None
    },
    'CHAT.CENTER': {
        'code': 51,
        'category': CATEGORIES[4],
        'id3v1': None,
        'id3v2': None
    },
    'VOTE.QUESTION': {
        'code': 52,
        'category': CATEGORIES[4],
        'id3v1': None,
        'id3v2': None
    },
    'VOTE.CENTRE': {
        'code': 53,
        'category': CATEGORIES[4],
        'id3v1': None,
        'id3v2': None
    },
    'DESCRIPTOR.PLACE': {
        'code': 59,
        'category': CATEGORIES[6],
        'id3v1': None,
        'id3v2': None
    },
    'DESCRIPTOR.APPOINTMENT': {
        'code': 60,
        'category': CATEGORIES[6],
        'id3v1': None,
        'id3v2': None
    },
    'DESCRIPTOR.IDENTIFIER': {
        'code': 61,
        'category': CATEGORIES[6],
        'id3v1': 'ISRC',
        'id3v2': 'TSRC'
    },
    'DESCRIPTOR.PURCHASE': {
        'code': 62,
        'category': CATEGORIES[6],
        'id3v1': 'WWWPAYMENT',
        'id3v2': 'WPAY'
    },
    'DESCRIPTOR.GET_DATA': {
        'code': 63,
        'category': CATEGORIES[6],
        'id3v1': None,
        'id3v2': None
    },
}

#: The maximum text limit in bytes according to ETSI TS 102 980, 5.0
MAXIMUM_TEXT_LIMIT = 128

class DLPlusError(Exception):
    """Base exception for DL Plus"""

class DLPlusMessageError(DLPlusError):
    """DL Plus message related exceptions"""

class DLPlusContentTypeError(DLPlusError):
    """DL Plus content type related exceptions"""

class DLPlusTagError(DLPlusError):
    """DL Plus tag related exceptions"""

class DLPlusObjectError(DLPlusError):
    """DL Plus object related exceptions"""


class DLPlusMessage(object):
    """Dynamic Label Plus (DL Plus) message

    This class supports parsing or building a DL Plus message string
    """

    def __init__(self):
        """Constructor for the DLPlusMessage

	Creates a new :class:`DLPlusMessage` object which can be used to parse
	or build a DL Plus message string.
	"""

        #: The format string from which the message will be built
        self.format_string = ''

        #: The formatted DL Plus message
        self._message = ''

        #: Dictionary holding the assigned DL Plus objects
        self._dlp_objects = {}

        #: Dictionary holding the assigned DL Plus tags
        self._dlp_tags = {}

        #: Status if the message was successfully parsed
        self._parsed = False

        #: Status if the message was successfully built
        self._built = False


    def add_dlp_object(self, dlp_object):
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
            raise DLPlusMessageError(
                "dlp_object has to be a DLPlusObject object")

        # Up to four DL Plus objects can be created from each DL message
        # according to ETSI TS 102 980, 5.1
        if len(self._dlp_objects) >= 4:
            raise DLPlusMessageError(
                "Only a maximum of 4 DLPlusObject objects can be added")

        # Use the content_type of the DL Plus object as the dictionary key
        self._dlp_objects[dlp_object.content_type] = dlp_object


    def get_dlp_objects(self):
        """Returns the associated DL Plus objects (:class:`DLPlusObject`)

        :return: Dictionary of :class:`DLPlusObject` objects.
        :rtype: dict
        """
        return self._dlp_objects


    def add_dlp_tag(self, dlp_tag):
        """Add a :class:`DLPlusTag` required for parsing the message

        This method is intended to be used before parsing a DL Plus Message.
        It allows one to add up to four :class:`DLPlusTag` objects which will
        support parsing the DL Plus message into :class:`DLPlusObject` objects.
        After adding all DL Plus tags, :meth:`DLPlusMessage.parse()` has to be
        called.

        :param DLPlusTag dlp_tag: The DL Plus Tag object to add
        :raises DLPlusMessageError: when `dlp_tag` is not a
                                    :class:`DLPlusTag` object, or the maximum
                                    of four :class:`DLPlusTag` objects where
                                    already added.
        """

        if not isinstance(dlp_tag, DLPlusTag):
            raise DLPlusMessageError('dlp_tag has to be a DLPlusTag object')

        # Up to four DL Plus tags can be created from each DL message
        # according to ETSI TS 102 980, 5.1
        if len(self._dlp_tags) >= 4:
            raise DLPlusMessageError(
                "Only a maximum of 4 DLPlusTag objects can be added")

        self._dlp_tags[dlp_tag.content_type] = dlp_tag


    def get_dlp_tags(self):
        """Returns the associated DL Plus tags (:class:`DLPlusTag`)

        :return: Dictionary of :class:`DLPlusTag` objects.
        :rtype: dict
        """
        return self._dlp_tags


    def parse(self, message):
        """Parsing a DL Plus `message` into DL Plus objects

        This method parses a given DL Plus `message` into zero or more DL Plus
        objects (:class:`DLPlusObject`), according to the associated DL Plus
        tags (:class:`DLPlusTag`).

        Before calling this method, one is supposed to add up to four expected
        DL Plus tags (:class:`DLPlusTag`) via the
        :meth:`DLPlusMessage.add_dlp_tag()` method.  Afterwards the newly
        created DL Plus objects (:class:`DLPlusObject`) can be retrieved via
        the :meth:`DLPlusMessage.get_dlp_objects()` method.

        :param str message: The DL Plus message string which should be parsed
        """

        # Reset the DLPlusObjects
        self._dlp_objects = {}

        # Extract sub strings from the message according to the DLPlusTag
        # objects to create DLPLusObject objects
        for content_type in self._dlp_tags:
            dlp_tag = self._dlp_tags[content_type]
            end = dlp_tag.start + dlp_tag.length

            # Delete objects have their length marker set to 0 and the start
            # marker set to a blank character, according to ETSI TS 102 980,
            # 6.2 Creating a delete object
            delete = bool(
                dlp_tag.length == 0 and message[dlp_tag.start:end+1] == ' ')

            self._dlp_objects[dlp_tag.content_type] = DLPlusObject(
                dlp_tag.content_type, message[dlp_tag.start:end], delete)

        self._message = message
        self._parsed = True


    def build(self, format_string):
        """Build a DL Plus message from a given format and DL Plus objects

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
        objects (:class:`DLPlusObject`) via the
        :meth:`DLPlusMessage.add_dlp_object()` method. Afterwards the newly
        created DL Plus tags (:class:`DLPlusTag`) can be retrieved via the
        :meth:`DLPlusMessage.get_dlp_tags()` method.

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
        if len(message.encode('utf-8')) > MAXIMUM_TEXT_LIMIT:
            raise DLPlusMessageError(
                'Message is longer than {} bytes'.format(MAXIMUM_TEXT_LIMIT))

        self._message = message

        # Reset the DLPlusTags
        self._dlp_tags = {}

        # Create DLPlusTags from the message and DLPlusObjects
        for content_type in self._dlp_objects:
            dlp_object = self._dlp_objects[content_type]
            self._dlp_tags[dlp_object.content_type] = DLPlusTag.from_message(
                self, dlp_object.content_type)

        self._built = True


    @property
    def message(self):
        """Getter for :attr:`_message`

        :return: Formatted DL Plus Message
        :rtype: str
        """
        return self._message


    def __str__(self):
        """Returns the formatted DL Plus Message

        :return: Formatted DL Plus Message
        :rtype: str
        """

        return self.message


class DLPlusContentType(object):
    """Dynamic Label Plus content type"""

    def __init__(self, content_type):
        """Constructor

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
            raise DLPlusContentTypeError(
                'Invalid content_type: {}'.format(content_type))

        #: The content type according to ETSI TS 102 980, Annex A, Table A.1
        self.content_type = content_type


    def get_code(self):
        """Get the content type code

        Returns the content type code according to ETSI TS 102 980, Annex A
        (List of DL Plus content types), Table A.1.

        :return: content type code
        :rtype: int
        """

        return CONTENT_TYPES[self.content_type]['code']


    def get_category(self):
        """Get the content type category

        Returns the content type category according to ETSI TS 102 980, Annex A
        (List of DL Plus content types), Table A.1.

        :return: category string
        :rtype: str
        """
        return CONTENT_TYPES[self.content_type]['category']


    def is_dummy(self):
        """Checks whether the instance is a "dummy" object

        Checks whether the :attr:`content_type`of the instance is set to `DUMMY`

        :return: `True` if the instance is a dummy object, otherwise `False`
        :rtype: bool
        """
        return bool(self.content_type == 'DUMMY')


    def __str__(self):
        """Returns the content type

        :return: DL Plus content type
        :rtype: str
        """
        return self.content_type


@python_2_unicode_compatible
class DLPlusObject(DLPlusContentType):
    """Dynamic Label Plus (DL Plus) object

    DL Plus object which holds a text string with a defined content type.
    """

    def __init__(self, content_type, text='', delete=False):
        """Constructor for a DL Plus Object

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
        super(DLPlusObject, self).__init__(content_type)

        # Make sure that the byte length of the text doesn't exceed the maximum
        # allowed limit.
        # https://stackoverflow.com/a/4013418/8587602
        if len(text.encode('utf-8')) > MAXIMUM_TEXT_LIMIT:
            raise DLPlusObjectError(
                'Text is longer than {} bytes'.format(MAXIMUM_TEXT_LIMIT))

        # DL Plus dummy objects always have their text set to an empty string
        if self.is_dummy():
            text = ''

        #: The text string of the DL Plus object
        self.text = text

        #: Flag which specifies whether the DL Plus object is a Delete object
        self.is_delete = delete

        #: The creation time stamp of the DL Plus object in UTC
        self.creation_ts = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

        #: The expiration (deletion) time stamp of the DL Plus object in UTC
        self.expiration_ts = None

    def expire(self):
        """Sets the expiration (deletion) time stamp to the current time in UTC

        This method should be called if the current DL Plus object gets updated
        by a new one or an explicit delete object has been received. It will set
        :attr:`expiration_ts` to a TZ aware :class:`datetime.datetime` object
        representing the current time in UTC.
        """
        self.expiration_ts = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

    @classmethod
    def create_dummy(cls):
        """Factory which creates a new dummy object

        The factory creates a new :class:`DLPlusObject` dummy object which has
        the content type set to `DUMMY` and the text string to an empty value.

        :return: Dummy DL Plus Object
        :rtype: DLPlusObject
        """

        return cls('DUMMY', '')


    def __str__(self):
        """Returns the DL Plus object's text

        :return: DL Plus object text
        :rtype: str
        """
        return self.text


@python_2_unicode_compatible
class DLPlusTag(DLPlusContentType):
    """Dynamic Label Plus (DL Plus) tag

    DL plus tag which defines a start and length marker together with a content
    type.
    """

    def __init__(self, content_type, start, length):
        """Constructor for a DL Plus tag

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
        super(DLPlusTag, self).__init__(content_type)

        if not isinstance(start, int) or start < 0:
            raise DLPlusTagError('start must be a positive integer')

        if not isinstance(length, int) or length < 0:
            raise DLPlusTagError('length must be a positive integer')


        self.content_type = content_type

        # Dummy objects always have their start and length marker set to 0
        if self.is_dummy():
            start = 0
            length = 0

        self.start = start
        self.length = length


    @classmethod
    def from_message(cls, dlp_message, content_type):
        """Factory which creates a new instance from a :class:`DLPlusMessage`

        The factory creates a new :class:`DLPlusTag` object from an existing
        and already populated :class:`DLPlusMessage` object, this way one
        doesn't has to calculate and specify the `start` and `length` markers.

        :param DLPlusMessage dlp_message: The populated DL Plus message
        :return: DL Plus Tag
        :rtype: DLPlusTag
        """

        # Pythonic factory class method according to:
        # * https://stackoverflow.com/a/14992545
        # * https://stackoverflow.com/a/12179752

        if not isinstance(dlp_message, DLPlusMessage):
            raise DLPlusTagError("dlp_message has to be a DLPlusMessage")

        if content_type not in CONTENT_TYPES:
            raise DLPlusContentTypeError(
                'Invalid content_type: {}'.format(content_type))

        # Check that a DLPlusObject object for the requested content type
        # was added and is available.
        try:
            dlp_object = dlp_message.get_dlp_objects()[content_type]
        except KeyError:
            raise DLPlusTagError(
                'No DLPlusObject for content type {} available'.format(
                    content_type))

        # Get the start marker (index) of the DL Plus object's text
        start = dlp_message.message.find(dlp_object.text)

        # Get the string length of the DL Plus object's text
        length = len(dlp_object.text)

        return cls(content_type, start, length)


    @classmethod
    def create_dummy(cls):
        """Factory which creates a new dummy instance

        The factory creates a new :class:`DLPlusTag` dummy instance which has
        the content type set to `DUMMY` and the start and length marker set to
        0 (zero).

        :return: Dummy DL Plus Tag
        :rtype: DLPlusTag
        """

        return cls('DUMMY', 0, 0)
