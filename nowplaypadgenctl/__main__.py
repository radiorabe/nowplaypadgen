"""Command line tool to interact with nowplaypadgen."""

import argparse
import logging
import os
import sys
from distutils.core import run_setup


def get_version() -> str:
    """Get version from setup.py."""
    return run_setup("./setup.py", stop_after="init").version


def parse_arguments():  # pragma: no cover
    """Parse arguments passed by user."""
    parser = argparse.ArgumentParser(description=__doc__)

    default_config = os.path.dirname(__file__) + "../nowplaypadgen.conf"

    parser.add_argument(
        "-c",
        "--config",
        action="store",
        default=default_config,
        help="Configuration file to use",
    )

    parser.add_argument("-s", "--show", action="store", help="The name of the show")

    parser.add_argument("-a", "--artist", action="store", help="The name of the artist")

    parser.add_argument(
        "-t", "--title", action="store", help="The title of the currently playing track"
    )

    version = get_version()
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {version}",
        help="Display the version",
    )

    parser.parse_args()


def setup_logging() -> logging.Logger:  # pragma: no cover
    """Prepare logger."""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler(stream=sys.stdout)

    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(
        logging.Formatter("%(levelname)s - %(name)s - %(message)s")
    )

    logger.addHandler(stream_handler)
    return logger


def main():  # pragma: no cover
    """Application entrypoint."""
    logger = setup_logging()
    parse_arguments()
    logger.info("hello world")


if __name__ == "__main__":  # pragma: no cover
    main()
