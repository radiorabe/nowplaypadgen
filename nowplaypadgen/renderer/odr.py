"""Convert to ODR-padenc style string prepresentation of Dynamic Label Plus strings.

This module generates a string/file that may be used with odr-padenc. odr-padenc
expects ether a simple DLS string or a string prefixed with a DLS header that
specifies the dynamic segments to be encoded into the mux.

More documentation on the odr-padenc format is available from <TODO>.
"""

from typing import Self

from nowplaypadgen.dlplus import DLPlusMessage


class ODRPadEncRenderer:
    """Manage ODR-padenc format."""

    def __init__(self, message: DLPlusMessage) -> None:
        """Create :class:`ODRPadEncRenderer` instance."""
        self._message = message
        super().__init__()

    @property
    def message(self: Self) -> DLPlusMessage:
        """Return messsage."""
        return self._message

    def __str__(self) -> str:
        """Render :class:`ODRPadEncRenderer` as a odr-padenc style string.

        @TODO ensure this matches what odr-padenc expects.

        Simple non labeled strings are output as is.

        >>> from nowplaypadgen.dlplus import DLPlusMessage, DLPlusObject
        >>> message = DLPlusMessage()
        >>> message.build("I am a message!")
        >>> odr = ODRPadEncRenderer(message)
        >>> str(odr)
        'I am a message!'

        If you add labels they are added in a odr-padenc style parameters frontmatter.

        >>> message.add_dlp_object(DLPlusObject("STATIONNAME.LONG", "Radio RaBe"))
        >>> message.add_dlp_object(DLPlusObject("STATIONNAME.SHORT", "RaBe"))
        >>> message.build("$STATIONNAME.LONG")
        >>> string = str(odr)
        >>> "##### parameters { #####" in string
        True
        >>> "DL_PLUS=1" in string
        True
        >>> "DL_PLUS_TAG=31 6 4" in string
        True
        >>> "DL_PLUS_TAG=32 0 10" in string
        True
        >>> "##### parameters } #####" in string
        True
        >>> "Radio RaBe" in string
        True

        :returns: String DLPlusMessage formatted for input to odr-dabenc.
        """
        dlp_tags = ""
        if self.message.get_dlp_tags():
            dlp_tags = "".join(
                (
                    "##### parameters { #####\n",
                    "DL_PLUS=1\n",
                    "".join(
                        {
                            f"DL_PLUS_TAG={tag.code} {tag.start} {tag.length}\n"
                            for (_, tag) in self.message.get_dlp_tags().items()
                        }
                    ),
                    "##### parameters } #####\n",
                )
            )
        return f"{dlp_tags}{self.message.message}"
