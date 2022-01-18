# -*- coding: utf-8 -*-
"""Test :class:`DLPlusMessage`."""

import pytest

from nowplaypadgen.dlplus import (
    DLPlusMessage,
    DLPlusMessageError,
    DLPlusObject,
    DLPlusTag,
)


@pytest.fixture(name="content_type")
def fixture_content_type():
    """Content type fixture."""
    return "ITEM.TITLE"


@pytest.fixture(name="title")
def fixture_title():
    """Title fixture."""
    return "My Titleö"


@pytest.fixture(name="artist")
def fixture_artist():
    """Artist fixture."""
    return "My Artistä"


@pytest.fixture(name="prefix")
def fixture_prefix():
    """Prefix fixture."""
    return "Now playing: "


@pytest.fixture(name="format_string")
def fixture_format_string(prefix):
    """Format string fixture."""
    return prefix + "${ITEM.TITLE} - ${ITEM.ARTIST}"


@pytest.fixture(name="title_start")
def fixture_title_start(prefix):
    """Title start fixture."""
    return len(prefix)


@pytest.fixture(name="title_length")
def fixture_title_length(title):
    """Title length fixture."""
    return len(title)


@pytest.fixture(name="artist_start")
def fixture_artist_start(title_start, title_length):
    """Artist start fixture."""
    return title_start + title_length + 3


@pytest.fixture(name="artist_length")
def fixture_artist_length(artist):
    """Artist length fixture."""
    return len(artist)


@pytest.fixture(name="mapping")
def fixture_mapping(title, artist):
    """Return mapping fixture."""
    return {"ITEM.TITLE": title, "ITEM.ARTIST": artist}


@pytest.fixture(name="title_content_type")
def fixture_title_content_type():
    """Title content type fixture."""
    return "ITEM.TITLE"


@pytest.fixture(name="artist_content_type")
def fixture_artist_content_type():
    """Artist content type fixture."""
    return "ITEM.ARTIST"


@pytest.fixture(name="dlp_title_obj")
def fixture_dlp_title_obj(title_content_type, title):
    """DLP title object fixture."""
    return DLPlusObject(title_content_type, title)


@pytest.fixture(name="dlp_artist_obj")
def fixture_dlp_artist_obj(artist_content_type, artist):
    """DLP artist object fixture."""
    return DLPlusObject(artist_content_type, artist)


@pytest.fixture(name="dlp_artist_tag")
def fixture_dlp_artist_tag(artist_content_type, artist_start, artist_length):
    """Artist tag fixture."""
    return DLPlusTag(artist_content_type, artist_start, artist_length)


@pytest.fixture(name="dlp_title_tag")
def fixture_dlp_title_tag(title_content_type, title_start, title_length):
    """Title tag fixture."""
    return DLPlusTag(title_content_type, title_start, title_length)


@pytest.fixture(name="dlp_msg")
def fixture_dlp_message():
    """Message fixture."""
    return DLPlusMessage()


def test_instance_creation(dlp_msg):
    """Test the creation of a new DL Plus Message."""
    assert isinstance(dlp_msg, DLPlusMessage)


def test_add_dlp_object(dlp_msg, dlp_title_obj, dlp_artist_obj):
    """Test that DL Plus Objects can be added and retrieved."""

    dlp_msg.add_dlp_object(dlp_title_obj)
    dlp_msg.add_dlp_object(dlp_artist_obj)

    dlp_objects = dlp_msg.get_dlp_objects()
    assert isinstance(dlp_objects, dict)

    assert "ITEM.TITLE" in dlp_objects
    assert dlp_objects["ITEM.TITLE"] == dlp_title_obj

    assert "ITEM.ARTIST" in dlp_objects
    assert dlp_objects["ITEM.ARTIST"] == dlp_artist_obj


def test_add_invalid_dlp_object(dlp_msg):
    """Test that only DLPlusObject objects can be added."""

    with pytest.raises(DLPlusMessageError) as dlplus_message_error:
        dlp_msg.add_dlp_object("not-a-DLPlusObject")

    expected_msg = "dlp_object has to be a DLPlusObject object"
    assert expected_msg in str(dlplus_message_error)


def test_maximum_dlp_objects(dlp_msg):
    """Test that no more than 4 DLPlusObject objects can be added."""

    dlp_objects_list = [
        DLPlusObject("ITEM.TITLE", "title"),
        DLPlusObject("ITEM.ALBUM", "album"),
        DLPlusObject("ITEM.TRACKNUMBER", "1"),
        DLPlusObject("ITEM.ARTIST", "artist"),
        DLPlusObject("ITEM.COMPOSITION", "composition"),
    ]

    with pytest.raises(DLPlusMessageError) as dlplus_message_error:
        for dlp_object in dlp_objects_list:
            dlp_msg.add_dlp_object(dlp_object)

    expected_msg = "Only a maximum of 4 DLPlusObject objects can be added"
    assert expected_msg in str(dlplus_message_error)


def test_add_dlp_tag(dlp_msg, dlp_title_tag, dlp_artist_tag):
    """Test that DL Plus tags can be added and retrieved."""

    dlp_msg.add_dlp_tag(dlp_title_tag)
    dlp_msg.add_dlp_tag(dlp_artist_tag)

    dlp_tags = dlp_msg.get_dlp_tags()
    assert isinstance(dlp_tags, dict)

    assert "ITEM.TITLE" in dlp_tags
    assert dlp_tags["ITEM.TITLE"] == dlp_title_tag

    assert "ITEM.ARTIST" in dlp_tags
    assert dlp_tags["ITEM.ARTIST"] == dlp_artist_tag


def test_add_invalid_dlp_tag(dlp_msg):
    """Test that only DLPlusTag objects can be added."""

    with pytest.raises(DLPlusMessageError) as dlplus_message_error:
        dlp_msg.add_dlp_tag("not-a-DLPlusTag")

    expected_msg = "dlp_tag has to be a DLPlusTag object"
    assert expected_msg in str(dlplus_message_error)


def test_maximum_dlp_tags(dlp_msg):
    """Test that no more than 4 DLPlusTag objects can be added."""

    dlp_tags_list = [
        DLPlusTag("ITEM.TITLE", 1, 10),
        DLPlusTag("ITEM.ALBUM", 12, 10),
        DLPlusTag("ITEM.TRACKNUMBER", 24, 10),
        DLPlusTag("ITEM.ARTIST", 36, 10),
        DLPlusTag("ITEM.COMPOSITION", 48, 10),
    ]

    with pytest.raises(DLPlusMessageError) as dlplus_message_error:
        for dlp_tag in dlp_tags_list:
            dlp_msg.add_dlp_tag(dlp_tag)

    expected_msg = "Only a maximum of 4 DLPlusTag objects can be added"
    assert expected_msg in str(dlplus_message_error)


def test_parse_message(
    dlp_msg, dlp_title_tag, dlp_artist_tag, title, artist
):  # pylint: disable=too-many-arguments
    """Test the parsing of a DL Plus message."""

    dlp_msg.add_dlp_tag(dlp_title_tag)
    dlp_msg.add_dlp_tag(dlp_artist_tag)

    dlp_msg.parse(f"Now playing: {title} - {artist}")

    dlp_objects = dlp_msg.get_dlp_objects()

    # A dictionary with two DLPlusObject objects is expected.
    assert isinstance(dlp_objects, dict)
    assert len(dlp_objects) == 2

    assert "ITEM.TITLE" in dlp_objects
    assert dlp_objects["ITEM.TITLE"].text == title
    assert not dlp_objects["ITEM.TITLE"].is_delete

    assert "ITEM.ARTIST" in dlp_objects
    assert dlp_objects["ITEM.ARTIST"].text == artist
    assert not dlp_objects["ITEM.ARTIST"].is_delete


def test_dlp_delete_object(dlp_msg):
    """Test the retrieval of a DL Plus delete object."""

    content_type = "INFO.NEWS"

    # Set the start marker to a blank character ('Now playing: ') and the
    # length marker to 0.
    dlp_delete_tag = DLPlusTag(content_type, 12, 0)
    dlp_msg.add_dlp_tag(dlp_delete_tag)

    dlp_msg.parse("Now playing: Never gonna give you up - Rick Astley")

    dlp_objects = dlp_msg.get_dlp_objects()

    # A dictionary with one DLPlusObject object that has the delete flag
    # set to True is expected.
    assert isinstance(dlp_objects, dict)
    assert content_type in dlp_objects
    assert dlp_objects[content_type].is_delete


def test_build_message(
    dlp_msg,
    dlp_title_obj,
    dlp_artist_obj,
    format_string,
    artist_start,
    artist_length,
    title_start,
    title_length,
    title,
    artist,
):  # pylint: disable=too-many-arguments
    """Test the building of a DL Plus message."""

    dlp_msg.add_dlp_object(dlp_title_obj)
    dlp_msg.add_dlp_object(dlp_artist_obj)

    dlp_msg.build(format_string)

    dlp_tags = dlp_msg.get_dlp_tags()

    # Check that the message was correctly built
    assert dlp_msg.message == f"Now playing: {title} - {artist}"

    # A dictionary with two DLPlusTag objects is expected.
    assert isinstance(dlp_tags, dict)
    assert len(dlp_tags) == 2

    # Test that the start and length markers are correct
    assert "ITEM.ARTIST" in dlp_tags
    assert dlp_tags["ITEM.ARTIST"].start == artist_start
    assert dlp_tags["ITEM.ARTIST"].length == artist_length

    # Test that the start and length markers are correct
    assert "ITEM.TITLE" in dlp_tags
    assert dlp_tags["ITEM.TITLE"].start == title_start
    assert dlp_tags["ITEM.TITLE"].length == title_length


def test_build_message_over_maximum_limit(dlp_msg, dlp_title_obj, dlp_artist_obj):
    """Test the building of a DL Plus message over the maximum limit."""

    dlp_msg.add_dlp_object(dlp_title_obj)
    dlp_msg.add_dlp_object(dlp_artist_obj)

    format_string = "".join("A" for _ in range(129))

    with pytest.raises(DLPlusMessageError) as dlplus_message_error:
        dlp_msg.build(format_string)

    expected_msg = "Message is longer than 128 bytes"
    assert expected_msg in str(dlplus_message_error)
