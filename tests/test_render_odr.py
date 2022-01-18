"""Test rendering of ODR-PadEnc style strings."""

from nowplaypadgen.dlplus import DLPlusMessage, DLPlusObject
from nowplaypadgen.renderer.odr import ODRPadEncRenderer


def test_render_odr():
    """Test the rendering of a DL Pluss message."""

    message = DLPlusMessage()
    message.add_dlp_object(DLPlusObject("ITEM.TITLE", "Radio Bern"))
    message.add_dlp_object(DLPlusObject("STATIONNAME.SHORT", "RaBe"))
    message.add_dlp_object(DLPlusObject("STATIONNAME.LONG", "Radio Bern RaBe"))
    message.build("$STATIONNAME.LONG")

    renderer = ODRPadEncRenderer(message)
    output = str(renderer)

    assert output.split("\n", maxsplit=1)[0] == "##### parameters { #####"
    assert output.split("\n")[1] == "DL_PLUS=1"
    assert output.split("\n")[5] == "##### parameters } #####"
    assert output.split("\n")[6] == "Radio Bern RaBe"

    assert "DL_PLUS_TAG=1 0 10" in output
    assert "DL_PLUS_TAG=31 11 4" in output
    assert "DL_PLUS_TAG=32 0 15" in output
