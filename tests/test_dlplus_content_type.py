"""Test :class:`DLPlusContentType`."""


import pytest

from nowplaypadgen.dlplus import DLPlusContentType, DLPlusContentTypeError


@pytest.fixture(name="content_type")
def fixture_content_type():
    """Content type fixture."""
    return "ITEM.TITLE"


def test_content_type_category():
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
        dlp_content_type = DLPlusContentType(content_type)
        assert dlp_content_type.category == category


def test_content_type_code():
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
        dlp_content_type = DLPlusContentType(content_type)
        assert dlp_content_type.code == code


def test_invalid_content_type():
    """Test that an invalid content type will be refused."""

    content_type = "MY.INVALID.TYPE"

    with pytest.raises(DLPlusContentTypeError) as dlplus_content_type_error:
        DLPlusContentType(content_type)

    assert f"Invalid content_type: {content_type}" in str(dlplus_content_type_error)
