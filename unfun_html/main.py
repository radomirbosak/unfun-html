# -*- coding: utf-8 -*-
"""
Main module
"""

import bs4
import rich
from rich.table import Table
import yaml


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


def naive_extract(soup, node_key):
    """Evaluate (tag/attr tuples)"""
    node_name, attr_name = node_key

    def node_conditions(node):
        avalue = node.attrs.get(attr_name)
        return node.name == node_name and \
            attr_name in node.attrs and \
            not isinstance(avalue, list)
    node = soup.find(node_conditions)
    if node is None:
        return None
    return node.attrs[attr_name]


def main():
    """Main entrypoint"""
    with open('data/Petersilie.yaml') as _f:
        word_targets = yaml.load(_f, Loader=yaml.BaseLoader)

    with open('data/Petersilie.html') as _f:
        word_soup = bs4.BeautifulSoup(_f, features='html.parser')

    kernels = naive_traversal(word_soup)

    print(f'Searching for: {word_targets["name"]}')

    table = Table()
    table.add_column('tag')
    table.add_column('attr', width=16)
    table.add_column('value', width=32)
    for tag, attribute in kernels:
        value = naive_extract(word_soup, (tag, attribute))
        table.add_row(tag, attribute, value)

    rich.print(table)
