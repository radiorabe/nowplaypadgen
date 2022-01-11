"""Audio Track module."""
from __future__ import annotations

from uuid import uuid4

import mutagen

from nowplaypadgen import timeperiod


class TrackError(Exception):
    """Track related exception."""


class Track(timeperiod.TimePeriod):
    """Track class which represents an audio track.

    A track has at least an artist, a title and an UUID. It can have a start
    time, an end time and a length as well as additional optional meta tags.

    Example::

        my_track = track.Track('Example Artist', 'Example Title')
        my_track.set_length(60) # The track has a one minute duration
    """

    def __init__(self, artist=None, title=None, uuid=uuid4()):
        """Create :class:`track.Track` instance.

        :param str artist: The artist of the track
        :param str title: The title of the track
        :param str uuid: The UUID of the track
        """

        self.artist = artist  #: The track's artist
        self.title = title  #: The track's title
        self.uuid = uuid  #: The track's global unique identifier (UUID)
        self.tags = {}  #: Optional meta tag dictionary of a track
        # Call the parent's constructor
        super().__init__()

    @classmethod
    def from_file(cls, track_path) -> Track:
        """Create Factory for creating a :class:`track.Track` object from a local file.

        The factory uses :class:`mutagen.File` to parse the meta data (tags and
        length) of the audio file and adds it to a new :class:`track.Track`
        object before returning it.

        :param str track_path: The file system path to the audio track
        :return: New :class:`track.Track` instance
        """
        # Pythonic factory class method according to:
        # * https://stackoverflow.com/a/14992545
        # * https://stackoverflow.com/a/12179752
        #
        # @TODO: This method should be removed from the main track class as we
        #        want to support more track loaders in the future. However, I'm
        #        not yet sure, which class structure and pattern I should use
        #        to achieve this. Decorate the class, create separate loader
        #        classes, use multiple factory classes?

        audio_file = mutagen.File(track_path)

        # Set first artist/title or assign None, if not present
        artist = audio_file.get("artist", [None])[0]
        title = audio_file.get("title", [None])[0]

        new_track = cls(artist, title)
        new_track.set_length(audio_file.info.length)

        # audio_file.items() returns a list of (tag) tuples
        # assign the tags to the new_track instance dictionary
        for tag_name, tag_value in audio_file.items():
            # Most of the tag values are returned as lists, as they might have
            # multiple values, we only support the first one here, to keep it
            # simple.
            if isinstance(tag_value, list):
                new_track.tags[tag_name] = tag_value[0]
            else:
                new_track.tags[tag_name] = tag_value

        return new_track

    def __str__(self) -> str:
        """Return a string representation of the track.

        Returns a string in the form of ``<ARTIST> - <TITLE> (<UUID>)`` useful
        for logging or a textual representation of the track.


        :return: String containing the track's artist and title
        """
        return f"Track: {self.artist} - {self.title} ({self.uuid})"
