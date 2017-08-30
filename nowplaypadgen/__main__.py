import nowplaypadgen
import argparse
import logging
import os
import sys


logger = logging.getLogger(__name__)

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='DAB+ now playing PAD (DLS+ and MOT SLS) generator'
    )

    default_config = os.path.dirname(__file__) + '../nowplaypadgen.conf'

    parser.add_argument('-c', '--config', action='store', 
                        default=default_config,
                        help='Configuration file to use')

    parser.add_argument('-s', '--show', action='store', 
                        help='The name of the show')

    parser.add_argument('-a', '--artist', action='store', 
                        help='The name of the artist')

    parser.add_argument('-t', '--title', action='store', 
                        help='The title of the currently playing track')

    parser.add_argument('-v', '--version', action='version',
                        version=nowplaypadgen.__version__,
                        help='Display the version')

    args = parser.parse_args()


def setup_logging():
    logger.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler(stream=sys.stdout)

    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter( \
        logging.Formatter('%(levelname)s - %(name)s - %(message)s'))

    logger.addHandler(stream_handler)
    logger.error('test')


def main():
    setup_logging()
    parse_arguments()
    logger.info('hello world')


if __name__ == "__main__":
    main()
