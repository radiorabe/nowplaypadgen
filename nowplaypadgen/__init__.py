"""DAB+ now playing PAG (DLS+ and MOT SLS generator)"""
from __future__ import unicode_literals

# Prevent "TypeError: Item in ``from list'' not a string" due to
# unicode_literals
__all__ = [str('show'), str('timeperiod')]
__version__ = '0.1.0'


class Error(Exception):
    """Base class for exceptions in this module."""
    pass
