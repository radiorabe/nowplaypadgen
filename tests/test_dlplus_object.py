"""Test :class:`DLPlusObject`."""

import datetime

import pytest
import pytz

from nowplaypadgen.dlplus import DLPlusContentType, DLPlusObject, DLPlusObjectError


@pytest.fixture(name="content_type")
def fixture_content_type():
    """Content type fixture."""
    return "ITEM.TITLE"


@pytest.fixture(name="text")
def fixture_text():
    """Text fixture."""
    return "My Title"


def test_instance_creation(content_type, text):
    """Test the creation of a new DL Plus Object."""

    dlp_object = DLPlusObject(content_type, text)

    assert isinstance(dlp_object, DLPlusObject)
    assert isinstance(dlp_object, DLPlusContentType)

    assert dlp_object.content_type == content_type
    assert dlp_object.text == text
    assert isinstance(dlp_object.creation_ts, datetime.datetime)

    # Assure that a TZ aware UTC datetime object is available
    assert dlp_object.creation_ts.tzinfo == pytz.utc
    assert dlp_object.creation_ts.tzinfo.utcoffset(dlp_object.creation_ts) is not None


def test_dummy_instance_creation():
    """Test the creation of a new DL Plus dummy object."""

    dlp_object = DLPlusObject.create_dummy()

    assert dlp_object.content_type == "DUMMY"
    assert dlp_object.text == ""
    assert dlp_object.is_dummy()


def test_dummy_has_empty_text():
    """Test that the text of a dummy object is set to an empty string."""

    dlp_object = DLPlusObject("DUMMY", "not an empty string")

    assert dlp_object.content_type == "DUMMY"
    assert dlp_object.text == ""


def test_delete_object(content_type, text):
    """Test the deletion of a DL Plus Object."""

    dlp_object = DLPlusObject(content_type, text)

    # Assure that the deletion time stamp is initially set to None
    assert dlp_object.expiration_ts is None

    # Expire the object by setting its deletion time stamp to the current
    # date and time in UTC
    dlp_object.expire()

    # Assure that a TZ aware UTC datetime object is available
    assert dlp_object.expiration_ts.tzinfo == pytz.utc
    assert dlp_object.creation_ts.tzinfo.utcoffset(dlp_object.creation_ts) is not None

    # Assure that the datetime object was set correctly
    now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
    assert dlp_object.expiration_ts <= now


def test_maximum_text_limit(content_type):
    """Test that a DL Plus Object's text can't be longer than 128 bytes."""

    # Up to a 128 bytes long DL Plus Object text must be supported
    max_length = 128

    # Generate a 128 character long unicode string, which will be encoded
    # to utf-8 within the DLPlusObject. A character out of the first 128
    # utf-8 code points is used, so that it will require exactly one byte
    # per character (128 characters => 128 bytes).
    text = "a" * max_length
    assert len(text.encode("utf-8")) == max_length

    dlp_object = DLPlusObject(content_type, text)
    assert isinstance(dlp_object, DLPlusObject)
    assert len(dlp_object.text.encode("utf-8")) == max_length

    # This text exceeds the limit by one byte and should fail
    long_text = "a" * (max_length + 1)
    assert len(long_text.encode("utf-8")) == max_length + 1

    with pytest.raises(DLPlusObjectError) as dlplus_object_error:
        DLPlusObject(content_type, long_text)

    assert f"Text is longer than {max_length} bytes" in str(dlplus_object_error)


def test_delete_object_creation(content_type, text):
    """Test the creation of a new DL Plus delete object."""

    dlp_object = DLPlusObject(content_type, text, True)

    assert dlp_object.is_delete
