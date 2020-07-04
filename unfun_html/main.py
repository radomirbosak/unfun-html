# -*- coding: utf-8 -*-
"""
Main module
"""

import bs4
import rich
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


def find_successful_kernel(soup, generator, extractor, target):
    """Return kernels which successfully extract the target for a single given soup"""
    return [kernel for kernel in generator(soup) if extractor(soup, kernel) == target]


def find_successful_kernel_for_dataset(dataset, generator, extractor):
    """
    Return kernels which successfully extract the target for a single given dataset

    dataset = list of (soup, target) tuples
    """
    # populate winner kernels
    semiwinner_list = []
    for soup, target in dataset:
        semi_winners = find_successful_kernel(soup, generator, extractor, target)
        semiwinner_list.append(semi_winners)

    if not semiwinner_list:
        return []

    # fetch kernels present in all datapoints
    winners = []
    for kernel in semiwinner_list[0]:
        if all(kernel in semi_winners for semi_winners in semiwinner_list):
            winners.append(kernel)
    return winners


def main():
    """Main entrypoint"""
    with open('data/Petersilie.yaml') as _f:
        word_targets = yaml.load(_f, Loader=yaml.BaseLoader)

    with open('data/Petersilie.html') as _f:
        word_soup = bs4.BeautifulSoup(_f, features='html.parser')

    # test finding successful kernel function
    winners = find_successful_kernel(word_soup, naive_traversal,
                                     naive_extract, word_targets["name"])
    rich.print("Winner kernels for 'name': ", winners)
