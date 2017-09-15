# -*- coding: utf-8 -*-
"""dlplus module related unit tests"""

from __future__ import unicode_literals

import datetime
import os
import sys
import unittest
import pytz

# Load the module locally from the dev environment.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from nowplaypadgen import dlplus # pylint: disable=wrong-import-position

class DLPlusContentTypeTestSuite(unittest.TestCase):
    """DLPlusContentType test cases."""

    def setUp(self):
        self.content_type = 'ITEM.TITLE'


    def test_content_type_category(self):
        """Test the content type categories"""

        content_types_to_categories = [
            ('DUMMY', 'Dummy'),
            ('ITEM.TITLE', 'Item'),
            ('INFO.NEWS', 'Info'),
            ('STATIONNAME.SHORT', 'Programme'),
            ('PHONE.HOTLINE', 'Interactivity'),
            ('DESCRIPTOR.PLACE', 'Descriptor')
        ]

        for content_type, category in content_types_to_categories:
            dlp_content_type = dlplus.DLPlusContentType(content_type)
            self.assertEqual(dlp_content_type.get_category(), category)


    def test_content_type_code(self):
        """Test the content type code"""

        content_types_to_codes = [
            ('DUMMY', 0),
            ('ITEM.TITLE', 1),
            ('INFO.NEWS', 12),
            ('STATIONNAME.SHORT', 31),
            ('PHONE.HOTLINE', 41),
            ('DESCRIPTOR.PLACE', 59)
        ]

        for content_type, code in content_types_to_codes:
            dlp_content_type = dlplus.DLPlusContentType(content_type)
            self.assertEqual(dlp_content_type.get_code(), code)


    def test_invalid_content_type(self):
        """Test that an invalid content type will be refused"""

        content_type = 'MY.INVALID.TYPE'

        with self.assertRaises(dlplus.DLPlusContentTypeError) as context_manager:
            _ = dlplus.DLPlusContentType(content_type)

        self.assertEqual('Invalid content_type: {}'.format(content_type),
                         str(context_manager.exception))


class DLPlusObjectTestSuite(unittest.TestCase):
    """DLPlusObject test cases."""

    def setUp(self):
        self.content_type = 'ITEM.TITLE'
        self.text = 'My Title'


    def test_instance_creation(self):
        """Test the creation of a new DL Plus Object"""

        dlp_object = dlplus.DLPlusObject(self.content_type, self.text)

        self.assertTrue(isinstance(dlp_object, dlplus.DLPlusObject))
        self.assertTrue(isinstance(dlp_object, dlplus.DLPlusContentType))

        self.assertEqual(dlp_object.content_type, self.content_type)
        self.assertEqual(dlp_object.text, self.text)
        self.assertTrue(isinstance(dlp_object.creation_ts, datetime.datetime))

        # Assure that a TZ aware UTC datetime object is available
        self.assertEqual(dlp_object.creation_ts.tzinfo, pytz.utc)
        self.assertTrue(
            dlp_object.creation_ts.tzinfo.utcoffset(dlp_object.creation_ts)
            is not None)


    def test_maximum_text_limit(self):
        """Test that a DL Plus Object's text can't be longer than 128 bytes"""

        # Up to a 128 bytes long DL Plus Object text must be supported
        max_length = 128

        # Generate a 128 character long unicode string, which will be encoded
        # to utf-8 within the DLPlusObject. A character out of the first 128
        # utf-8 code points is used, so that it will require exactly one byte
        # per character (128 characters => 128 bytes).
        text = 'a' * max_length
        self.assertEqual(len(text.encode('utf-8')), max_length)

        dlp_object = dlplus.DLPlusObject(self.content_type, text)
        self.assertTrue(isinstance(dlp_object, dlplus.DLPlusObject))
        self.assertEqual(len(dlp_object.text.encode('utf-8')), max_length)


        # This text exceeds the limit by one byte and should fail
        text = 'a' * (max_length + 1)
        self.assertEqual(len(text.encode('utf-8')), max_length + 1)

        with self.assertRaises(dlplus.DLPlusObjectError) as context_manager:
            _ = dlplus.DLPlusObject(self.content_type, text)

        self.assertEqual('Text is longer than {} bytes'.format(max_length),
                         str(context_manager.exception))



class DLPlusTagTestSuite(unittest.TestCase):
    """DLPlusTag test cases."""

    def setUp(self):
        self.content_type = 'ITEM.TITLE'
        self.start = 5
        self.length = 10


    def test_instance_creation(self):
        """Test the creation of a new DL Plus Tag"""

        dlp_tag = dlplus.DLPlusTag(self.content_type, self.start, self.length)

        self.assertTrue(isinstance(dlp_tag, dlplus.DLPlusTag))
        self.assertTrue(isinstance(dlp_tag, dlplus.DLPlusContentType))

        self.assertEqual(dlp_tag.content_type, self.content_type)
        self.assertEqual(dlp_tag.start, self.start)
        self.assertEqual(dlp_tag.length, self.length)


    def test_invalid_start(self):
        """Test that a DL Plus Tag start marker must be a postive integer"""

        expected_error_msg = 'start must be a positive integer'

        # No integer was passed
        with self.assertRaises(dlplus.DLPlusTagError) as context_manager:
            _ = dlplus.DLPlusTag(
                self.content_type, 'not-an-integer', self.length)

        self.assertEqual(expected_error_msg, str(context_manager.exception))

        # A negative integer was passed
        with self.assertRaises(dlplus.DLPlusTagError) as context_manager:
            _ = dlplus.DLPlusTag(self.content_type, -123, self.length)

        self.assertEqual(expected_error_msg, str(context_manager.exception))


    def test_invalid_length(self):
        """Test that a DL Plus Tag length marker must be a postive integer"""

        expected_error_msg = 'length must be a positive integer'

        # No integer was passed
        with self.assertRaises(dlplus.DLPlusTagError) as context_manager:
            _ = dlplus.DLPlusTag(self.content_type, self.start, 'not-an-integer')

        self.assertEqual(expected_error_msg, str(context_manager.exception))

        # A negative integer was passed
        with self.assertRaises(dlplus.DLPlusTagError) as context_manager:
            _ = dlplus.DLPlusTag(self.content_type, self.start, -123)

        self.assertEqual(expected_error_msg, str(context_manager.exception))


if __name__ == '__main__':
    unittest.main()
