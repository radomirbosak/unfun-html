# -*- coding: utf-8 -*-
"""
Main module
"""
import argparse
import sys

from .__version__ import __version__


def function():
    """Sample function"""
    print('Sample package')


def parse_args():
    """Parse CLI arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-V', '--version', action='store_true',
                        help='print program version')

    return parser.parse_args()


def main():
    """Main entrypoint"""
    # handle the --version switch
    if '--version' in sys.argv or 'V' in sys.argv:
        print('mypackage ' + __version__)
        sys.exit(0)

    # parse normal arguments
    parse_args()

    function()

    sys.exit(0)
