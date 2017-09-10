"""dlplus module related unit tests"""

import datetime
import os
import sys
import unittest
import pytz

# Load the module locally from the dev environment.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from nowplaypadgen import dlplus # pylint: disable=wrong-import-position


class DLPlusObjectTestSuite(unittest.TestCase):
    """DLPlusObject test cases."""

    def setUp(self):
        self.content_type = 'ITEM.TITLE'
        self.text = 'My Title'


    def test_instance_creation(self):
        """Test the creation of a new DL Plus Object"""

        dlp_object = dlplus.DLPlusObject(self.content_type, self.text)

        self.assertTrue(isinstance(dlp_object, dlplus.DLPlusObject))
        self.assertEqual(dlp_object.content_type, self.content_type)
        self.assertEqual(dlp_object.text, self.text)
        self.assertTrue(isinstance(dlp_object.creation_ts, datetime.datetime))

        # Assure that a TZ aware UTC datetime object is available
        self.assertEqual(dlp_object.creation_ts.tzinfo, pytz.utc)
        self.assertTrue(
            dlp_object.creation_ts.tzinfo.utcoffset(dlp_object.creation_ts)
            is not None)


    def test_content_type_category(self):
        """Test the content type categories of a DL Plus Object"""

        content_types_to_categories = [
            ('DUMMY', 'Dummy'),
            ('ITEM.TITLE', 'Item'),
            ('INFO.NEWS', 'Info'),
            ('STATIONNAME.SHORT', 'Programme'),
            ('PHONE.HOTLINE', 'Interactivity'),
            ('DESCRIPTOR.PLACE', 'Descriptor')
        ]

        for content_type, category in content_types_to_categories:
            dlp_object = dlplus.DLPlusObject(content_type, self.text)
            self.assertEqual(dlp_object.get_category(), category)


    def test_content_type_code(self):
        """Test the content type code of a DL Plus Object"""

        content_types_to_codes = [
            ('DUMMY', 0),
            ('ITEM.TITLE', 1),
            ('INFO.NEWS', 12),
            ('STATIONNAME.SHORT', 31),
            ('PHONE.HOTLINE', 41),
            ('DESCRIPTOR.PLACE', 59)
        ]

        for content_type, code in content_types_to_codes:
            dlp_object = dlplus.DLPlusObject(content_type, self.text)
            self.assertEqual(dlp_object.get_code(), code)


if __name__ == '__main__':
    unittest.main()
