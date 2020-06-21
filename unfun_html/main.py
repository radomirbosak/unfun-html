# -*- coding: utf-8 -*-
"""
Main module
"""
import argparse
import sys

import bs4
import yaml

from .__version__ import __version__


def function():
    """Sample function"""
    print('Sample package')


def naive_traversal(soup):
    """Traverse all tags with attributes"""
    visited = set()
    for tag in soup.descendants:
        bad_node_types = [bs4.Doctype, bs4.Comment, bs4.NavigableString]
        if any(isinstance(tag, bad) for bad in bad_node_types):
            continue
        for attr in tag.attrs.keys():
            node_key = (tag.name, attr)
            if node_key in visited:
                continue
            yield node_key
            visited.add(node_key)


def parse_args():
    """Parse CLI arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-V', '--version', action='store_true',
                        help='print program version')

    return parser.parse_args()


def main():
    """Main entrypoint"""
    with open('data/Petersilie.yaml') as _f:
        word_targets = yaml.load(_f, Loader=yaml.BaseLoader)

    with open('data/Petersilie.html') as _f:
        word_soup = bs4.BeautifulSoup(_f, features='html.parser')

    kernels = naive_traversal(word_soup)

    print(f'Searching for: {word_targets["name"]}')
    print()
    print('tag\tattribute')
    print('===\t=========')
    for tag, attribute in kernels:
        # print(f'<{tag} {attribute}="">')
        print(f"{tag}\t{attribute}")
