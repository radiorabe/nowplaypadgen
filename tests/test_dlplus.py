# -*- coding: utf-8 -*-
"""dlplus module related unit tests."""

from __future__ import unicode_literals

import datetime
import os
import sys
import unittest

import pytz

from nowplaypadgen import dlplus

# Load the module locally from the dev environment.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class DLPlusContentTypeTestSuite(unittest.TestCase):
    """DLPlusContentType test cases."""

    def setUp(self):
        self.content_type = "ITEM.TITLE"

    def test_content_type_category(self):
        """Test the content type categories."""

        content_types_to_categories = [
            ("DUMMY", "Dummy"),
            ("ITEM.TITLE", "Item"),
            ("INFO.NEWS", "Info"),
            ("STATIONNAME.SHORT", "Programme"),
            ("PHONE.HOTLINE", "Interactivity"),
            ("DESCRIPTOR.PLACE", "Descriptor"),
        ]

        for content_type, category in content_types_to_categories:
            dlp_content_type = dlplus.DLPlusContentType(content_type)
            self.assertEqual(dlp_content_type.get_category(), category)

    def test_content_type_code(self):
        """Test the content type code."""

        content_types_to_codes = [
            ("DUMMY", 0),
            ("ITEM.TITLE", 1),
            ("INFO.NEWS", 12),
            ("STATIONNAME.SHORT", 31),
            ("PHONE.HOTLINE", 41),
            ("DESCRIPTOR.PLACE", 59),
        ]

        for content_type, code in content_types_to_codes:
            dlp_content_type = dlplus.DLPlusContentType(content_type)
            self.assertEqual(dlp_content_type.get_code(), code)

    def test_invalid_content_type(self):
        """Test that an invalid content type will be refused."""

        content_type = "MY.INVALID.TYPE"

        with self.assertRaises(dlplus.DLPlusContentTypeError) as context_manager:
            dlplus.DLPlusContentType(content_type)

        self.assertEqual(
            f"Invalid content_type: {content_type}", str(context_manager.exception)
        )


class DLPlusObjectTestSuite(unittest.TestCase):
    """DLPlusObject test cases."""

    def setUp(self):
        self.content_type = "ITEM.TITLE"
        self.text = "My Title"

    def test_instance_creation(self):
        """Test the creation of a new DL Plus Object."""

        dlp_object = dlplus.DLPlusObject(self.content_type, self.text)

        self.assertTrue(isinstance(dlp_object, dlplus.DLPlusObject))
        self.assertTrue(isinstance(dlp_object, dlplus.DLPlusContentType))

        self.assertEqual(dlp_object.content_type, self.content_type)
        self.assertEqual(dlp_object.text, self.text)
        self.assertTrue(isinstance(dlp_object.creation_ts, datetime.datetime))

        # Assure that a TZ aware UTC datetime object is available
        self.assertEqual(dlp_object.creation_ts.tzinfo, pytz.utc)
        self.assertTrue(
            dlp_object.creation_ts.tzinfo.utcoffset(dlp_object.creation_ts) is not None
        )

    def test_dummy_instance_creation(self):
        """Test the creation of a new DL Plus dummy object."""

        dlp_object = dlplus.DLPlusObject.create_dummy()

        self.assertEqual(dlp_object.content_type, "DUMMY")
        self.assertEqual(dlp_object.text, "")
        self.assertTrue(dlp_object.is_dummy())

    def test_dummy_has_empty_text(self):
        """Test that the text of a dummy object is set to an empty string."""

        dlp_object = dlplus.DLPlusObject("DUMMY", "not an empty string")

        self.assertEqual(dlp_object.content_type, "DUMMY")
        self.assertEqual(dlp_object.text, "")

    def test_delete_object(self):
        """Test the deletion of a DL Plus Object."""

        dlp_object = dlplus.DLPlusObject(self.content_type, self.text)

        # Assure that the deletion time stamp is initially set to None
        self.assertIsNone(dlp_object.expiration_ts)

        # Expire the object by setting its deletion time stamp to the current
        # date and time in UTC
        dlp_object.expire()

        # Assure that a TZ aware UTC datetime object is available
        self.assertEqual(dlp_object.expiration_ts.tzinfo, pytz.utc)
        self.assertIsNotNone(
            dlp_object.creation_ts.tzinfo.utcoffset(dlp_object.creation_ts)
        )

        # Assure that the datetime object was set correctly
        now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        self.assertTrue(dlp_object.expiration_ts <= now)

    def test_maximum_text_limit(self):
        """Test that a DL Plus Object's text can't be longer than 128 bytes."""

        # Up to a 128 bytes long DL Plus Object text must be supported
        max_length = 128

        # Generate a 128 character long unicode string, which will be encoded
        # to utf-8 within the DLPlusObject. A character out of the first 128
        # utf-8 code points is used, so that it will require exactly one byte
        # per character (128 characters => 128 bytes).
        text = "a" * max_length
        self.assertEqual(len(text.encode("utf-8")), max_length)

        dlp_object = dlplus.DLPlusObject(self.content_type, text)
        self.assertTrue(isinstance(dlp_object, dlplus.DLPlusObject))
        self.assertEqual(len(dlp_object.text.encode("utf-8")), max_length)

        # This text exceeds the limit by one byte and should fail
        text = "a" * (max_length + 1)
        self.assertEqual(len(text.encode("utf-8")), max_length + 1)

        with self.assertRaises(dlplus.DLPlusObjectError) as context_manager:
            dlplus.DLPlusObject(self.content_type, text)

        self.assertEqual(
            f"Text is longer than {max_length} bytes", str(context_manager.exception)
        )

    def test_delete_object_creation(self):
        """Test the creation of a new DL Plus delete object."""

        dlp_object = dlplus.DLPlusObject(self.content_type, self.text, True)

        self.assertTrue(dlp_object.is_delete)


class DLPlusTagTestSuite(unittest.TestCase):
    """DLPlusTag test cases."""

    def setUp(self):
        self.content_type = "ITEM.TITLE"
        self.start = 5
        self.length = 10

    def test_instance_creation(self):
        """Test the creation of a new DL Plus Tag."""

        dlp_tag = dlplus.DLPlusTag(self.content_type, self.start, self.length)

        self.assertTrue(isinstance(dlp_tag, dlplus.DLPlusTag))
        self.assertTrue(isinstance(dlp_tag, dlplus.DLPlusContentType))

        self.assertEqual(dlp_tag.content_type, self.content_type)
        self.assertEqual(dlp_tag.start, self.start)
        self.assertEqual(dlp_tag.length, self.length)

    def test_dummy_instance_creation(self):
        """Test the creation of a new DL Plus dummy Tag."""

        dlp_tag = dlplus.DLPlusTag.create_dummy()

        self.assertEqual(dlp_tag.content_type, "DUMMY")
        self.assertEqual(dlp_tag.start, 0)
        self.assertEqual(dlp_tag.length, 0)
        self.assertTrue(dlp_tag.is_dummy())

    def test_dummy_start_end_marker(self):
        """Test that the start and end marker of a dummy tag will be set to 0."""

        dlp_tag = dlplus.DLPlusTag("DUMMY", 10, 20)

        self.assertEqual(dlp_tag.content_type, "DUMMY")
        self.assertEqual(dlp_tag.start, 0)
        self.assertEqual(dlp_tag.length, 0)

    def test_invalid_start(self):
        """Test that a DL Plus Tag start marker must be a postive integer."""

        expected_msg = "start must be a positive integer"

        # No integer was passed
        with self.assertRaises(dlplus.DLPlusTagError) as context_manager:
            dlplus.DLPlusTag(self.content_type, "not-an-integer", self.length)

        self.assertEqual(expected_msg, str(context_manager.exception))

        # A negative integer was passed
        with self.assertRaises(dlplus.DLPlusTagError) as context_manager:
            dlplus.DLPlusTag(self.content_type, -123, self.length)

        self.assertEqual(expected_msg, str(context_manager.exception))

    def test_invalid_length(self):
        """Test that a DL Plus Tag length marker must be a postive integer."""

        expected_msg = "length must be a positive integer"

        # No integer was passed
        with self.assertRaises(dlplus.DLPlusTagError) as context_manager:
            dlplus.DLPlusTag(self.content_type, self.start, "not-an-integer")

        self.assertEqual(expected_msg, str(context_manager.exception))

        # A negative integer was passed
        with self.assertRaises(dlplus.DLPlusTagError) as context_manager:
            dlplus.DLPlusTag(self.content_type, self.start, -123)

        self.assertEqual(expected_msg, str(context_manager.exception))


class DLPlusMessageTestSuite(unittest.TestCase):
    """DLPlusMessage test cases."""

    # pylint: disable=too-many-instance-attributes
    # It's convenient to have all those public attributes here, rather
    # than re-defining them on each test-case.
    def setUp(self):

        self.title = "My Titleö"
        self.artist = "My Artistä"

        prefix = "Now playing: "
        self.format_string = prefix + "{o[ITEM.TITLE]} - {o[ITEM.ARTIST]}"

        self.title_start = len(prefix)
        self.title_length = len(self.title)

        self.artist_start = self.title_start + self.title_length + 3
        self.artist_length = len(self.artist)

        mapping = {"ITEM.TITLE": self.title, "ITEM.ARTIST": self.artist}
        self.message_string = self.format_string.format(o=mapping)

        self.title_content_type = "ITEM.TITLE"
        self.artist_content_type = "ITEM.ARTIST"

        self.dlp_title_obj = dlplus.DLPlusObject(self.title_content_type, self.title)

        self.dlp_artist_obj = dlplus.DLPlusObject(self.artist_content_type, self.artist)

        self.dlp_artist_tag = dlplus.DLPlusTag(
            self.artist_content_type, self.artist_start, self.artist_length
        )

        self.dlp_title_tag = dlplus.DLPlusTag(
            self.title_content_type, self.title_start, self.title_length
        )

        self.dlp_msg = dlplus.DLPlusMessage()

    def test_instance_creation(self):
        """Test the creation of a new DL Plus Message."""

        self.assertTrue(isinstance(self.dlp_msg, dlplus.DLPlusMessage))

    def test_add_dlp_object(self):
        """Test that DL Plus Objects can be added and retrieved."""

        self.dlp_msg.add_dlp_object(self.dlp_title_obj)
        self.dlp_msg.add_dlp_object(self.dlp_artist_obj)

        dlp_objects = self.dlp_msg.get_dlp_objects()
        self.assertTrue(isinstance(dlp_objects, dict))

        self.assertTrue("ITEM.TITLE" in dlp_objects)
        self.assertEqual(dlp_objects["ITEM.TITLE"], self.dlp_title_obj)

        self.assertTrue("ITEM.ARTIST" in dlp_objects)
        self.assertEqual(dlp_objects["ITEM.ARTIST"], self.dlp_artist_obj)

    def test_add_invalid_dlp_object(self):
        """Test that only DLPlusObject objects can be added."""

        with self.assertRaises(dlplus.DLPlusMessageError) as context_manager:
            self.dlp_msg.add_dlp_object("not-a-DLPlusObject")

        expected_msg = "dlp_object has to be a DLPlusObject object"
        self.assertEqual(expected_msg, str(context_manager.exception))

    def test_maximum_dlp_objects(self):
        """Test that no more than 4 DLPlusObject objects can be added."""

        dlp_objects_list = [
            dlplus.DLPlusObject("ITEM.TITLE", "title"),
            dlplus.DLPlusObject("ITEM.ALBUM", "album"),
            dlplus.DLPlusObject("ITEM.TRACKNUMBER", "1"),
            dlplus.DLPlusObject("ITEM.ARTIST", "artist"),
            dlplus.DLPlusObject("ITEM.COMPOSITION", "composition"),
        ]

        with self.assertRaises(dlplus.DLPlusMessageError) as context_manager:
            for dlp_object in dlp_objects_list:
                self.dlp_msg.add_dlp_object(dlp_object)

        expected_msg = "Only a maximum of 4 DLPlusObject objects can be added"
        self.assertEqual(expected_msg, str(context_manager.exception))

    def test_add_dlp_tag(self):
        """Test that DL Plus tags can be added and retrieved."""

        self.dlp_msg.add_dlp_tag(self.dlp_title_tag)
        self.dlp_msg.add_dlp_tag(self.dlp_artist_tag)

        dlp_tags = self.dlp_msg.get_dlp_tags()
        self.assertTrue(isinstance(dlp_tags, dict))

        self.assertTrue("ITEM.TITLE" in dlp_tags)
        self.assertEqual(dlp_tags["ITEM.TITLE"], self.dlp_title_tag)

        self.assertTrue("ITEM.ARTIST" in dlp_tags)
        self.assertEqual(dlp_tags["ITEM.ARTIST"], self.dlp_artist_tag)

    def test_add_invalid_dlp_tag(self):
        """Test that only DLPlusTag objects can be added."""

        with self.assertRaises(dlplus.DLPlusMessageError) as context_manager:
            self.dlp_msg.add_dlp_tag("not-a-DLPlusTag")

        expected_msg = "dlp_tag has to be a DLPlusTag object"
        self.assertEqual(expected_msg, str(context_manager.exception))

    def test_maximum_dlp_tags(self):
        """Test that no more than 4 DLPlusTag objects can be added."""

        dlp_tags_list = [
            dlplus.DLPlusTag("ITEM.TITLE", 1, 10),
            dlplus.DLPlusTag("ITEM.ALBUM", 12, 10),
            dlplus.DLPlusTag("ITEM.TRACKNUMBER", 24, 10),
            dlplus.DLPlusTag("ITEM.ARTIST", 36, 10),
            dlplus.DLPlusTag("ITEM.COMPOSITION", 48, 10),
        ]

        with self.assertRaises(dlplus.DLPlusMessageError) as context_manager:
            for dlp_tag in dlp_tags_list:
                self.dlp_msg.add_dlp_tag(dlp_tag)

        expected_msg = "Only a maximum of 4 DLPlusTag objects can be added"
        self.assertEqual(expected_msg, str(context_manager.exception))

    def test_parse_message(self):
        """Test the parsing of a DL Plus message."""

        self.dlp_msg.add_dlp_tag(self.dlp_title_tag)
        self.dlp_msg.add_dlp_tag(self.dlp_artist_tag)

        self.dlp_msg.parse(self.message_string)

        dlp_objects = self.dlp_msg.get_dlp_objects()

        # A dictionary with two DLPlusObject objects is expected.
        self.assertTrue(isinstance(dlp_objects, dict))
        self.assertEqual(len(dlp_objects), 2)

        self.assertTrue("ITEM.TITLE" in dlp_objects)
        self.assertEqual(dlp_objects["ITEM.TITLE"].text, self.title)
        self.assertFalse(dlp_objects["ITEM.TITLE"].is_delete)

        self.assertTrue("ITEM.ARTIST" in dlp_objects)
        self.assertEqual(dlp_objects["ITEM.ARTIST"].text, self.artist)
        self.assertFalse(dlp_objects["ITEM.ARTIST"].is_delete)

    def test_dlp_delete_object(self):
        """Test the retrieval of a DL Plus delete object."""

        content_type = "INFO.NEWS"

        # Set the start marker to a blank character ('Now playing: ') and the
        # length marker to 0.
        dlp_delete_tag = dlplus.DLPlusTag(content_type, 12, 0)
        self.dlp_msg.add_dlp_tag(dlp_delete_tag)

        self.dlp_msg.parse(self.message_string)

        dlp_objects = self.dlp_msg.get_dlp_objects()

        # A dictionary with one DLPlusObject object that has the delete flag
        # set to True is expected.
        self.assertTrue(isinstance(dlp_objects, dict))
        self.assertTrue(content_type in dlp_objects)
        self.assertTrue(dlp_objects[content_type].is_delete)

    def test_build_message(self):
        """Test the building of a DL Plus message."""

        self.dlp_msg.add_dlp_object(self.dlp_title_obj)
        self.dlp_msg.add_dlp_object(self.dlp_artist_obj)

        self.dlp_msg.build(self.format_string)

        dlp_tags = self.dlp_msg.get_dlp_tags()

        # Check that the message was correctly built
        self.assertEqual(self.dlp_msg.message, self.message_string)

        # A dictionary with two DLPlusTag objects is expected.
        self.assertTrue(isinstance(dlp_tags, dict))
        self.assertEqual(len(dlp_tags), 2)

        # Test that the start and length markers are correct
        self.assertTrue("ITEM.ARTIST" in dlp_tags)
        self.assertEqual(dlp_tags["ITEM.ARTIST"].start, self.artist_start)
        self.assertEqual(dlp_tags["ITEM.ARTIST"].length, self.artist_length)

        # Test that the start and length markers are correct
        self.assertTrue("ITEM.TITLE" in dlp_tags)
        self.assertEqual(dlp_tags["ITEM.TITLE"].start, self.title_start)
        self.assertEqual(dlp_tags["ITEM.TITLE"].length, self.title_length)


if __name__ == "__main__":
    unittest.main()
