"""Test :class:`DLPlusTag`."""


import pytest

from nowplaypadgen.dlplus import (
    DLPlusContentType,
    DLPlusContentTypeError,
    DLPlusMessage,
    DLPlusObject,
    DLPlusTag,
    DLPlusTagError,
)


@pytest.fixture(name="content_type")
def fixture_content_type():
    """Content type fixture."""
    return "ITEM.TITLE"


@pytest.fixture(name="start")
def fixture_start():
    """Start fixture."""
    return 5


@pytest.fixture(name="length")
def fixture_length():
    """Length fixture."""
    return 10


def test_instance_creation(content_type, start, length):
    """Test the creation of a new DL Plus Tag."""

    dlp_tag = DLPlusTag(content_type, start, length)

    assert isinstance(dlp_tag, DLPlusTag)
    assert isinstance(dlp_tag, DLPlusContentType)

    assert dlp_tag.content_type == content_type
    assert dlp_tag.start == start
    assert dlp_tag.length == length


def test_dummy_instance_creation():
    """Test the creation of a new DL Plus dummy Tag."""

    dlp_tag = DLPlusTag.create_dummy()

    assert dlp_tag.content_type == "DUMMY"
    assert dlp_tag.start == 0
    assert dlp_tag.length == 0
    assert dlp_tag.is_dummy()


def test_dummy_start_end_marker():
    """Test that the start and end marker of a dummy tag will be set to 0."""

    dlp_tag = DLPlusTag("DUMMY", 10, 20)

    assert dlp_tag.content_type == "DUMMY"
    assert dlp_tag.start == 0
    assert dlp_tag.length == 0


def test_invalid_start(content_type, length):
    """Test that a DL Plus Tag start marker must be a postive integer."""

    expected_msg = "start must be a positive integer"

    # No integer was passed
    with pytest.raises(DLPlusTagError) as dlplus_tag_error:
        DLPlusTag(content_type, "not-an-integer", length)

    assert expected_msg in str(dlplus_tag_error)

    # A negative integer was passed
    with pytest.raises(DLPlusTagError) as dlplus_tag_error:
        DLPlusTag(content_type, -123, length)

    assert expected_msg in str(dlplus_tag_error)


def test_invalid_length(content_type, start):
    """Test that a DL Plus Tag length marker must be a postive integer."""

    expected_msg = "length must be a positive integer"

    # No integer was passed
    with pytest.raises(DLPlusTagError) as dlplus_tag_error:
        DLPlusTag(content_type, start, "not-an-integer")

    assert expected_msg in str(dlplus_tag_error)

    # A negative integer was passed
    with pytest.raises(DLPlusTagError) as dlplus_tag_error:
        DLPlusTag(content_type, start, -123)

    assert expected_msg in str(dlplus_tag_error)


def test_from_message_invalid_message():
    """Test the creation of a DLPlusTag object from an invalid message."""

    with pytest.raises(DLPlusTagError) as dlplus_tag_error:
        DLPlusTag.from_message(None, "ITEM.TITLE")

    expected_msg = "dlp_message has to be a DLPlusMessage"
    assert expected_msg in str(dlplus_tag_error)


def test_from_message_invalid_content_type():
    """Test the creation of a DLPlusTag object from an invalid content type."""

    with pytest.raises(DLPlusContentTypeError) as dlplus_content_type_error:
        DLPlusTag.from_message(DLPlusMessage(), "HAHA.LOLWAT")

    expected_msg = "Invalid content_type: HAHA.LOLWAT"
    assert expected_msg in str(dlplus_content_type_error)


def test_from_message_missing_content_type():
    """Test the creation of a DLPlusTag object with a missing content type."""

    with pytest.raises(DLPlusTagError) as dlplus_tag_error:
        message = DLPlusMessage()
        message.add_dlp_object(DLPlusObject("STATIONNAME.LONG", "Radio RaBe"))
        DLPlusTag.from_message(message, "ITEM.TITLE")

    expected_msg = "No DLPlusObject for content type ITEM.TITLE available"
    assert expected_msg in str(dlplus_tag_error)
