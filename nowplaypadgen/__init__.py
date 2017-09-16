"""DAB+ now playing PAD (DLS+ and MOT SLS generator)"""
from __future__ import unicode_literals
from future.utils import python_2_unicode_compatible

# Prevent "TypeError: Item in ``from list'' not a string" due to
# unicode_literals
__all__ = [str(x) for x in ('show', 'timeperiod')]
__version__ = '0.1.0'


class Error(Exception):
    """Base class for exceptions in this module."""
    pass
