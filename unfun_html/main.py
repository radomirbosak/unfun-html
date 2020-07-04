# -*- coding: utf-8 -*-
"""
Main module
"""
import os

import bs4
import rich
import yaml


def load_data(data_dir):
    """Load yaml and html files from given data dir and pair them"""
    data = []
    for filename in os.listdir(data_dir):
        targets_path = os.path.join(data_dir, filename)

        # read only yaml files
        if not filename.endswith('.yaml'):
            continue

        # store real and expected result
        with open(targets_path, 'r') as f:
            target = yaml.load(f, Loader=yaml.SafeLoader)

        soup_path = targets_path[:-4] + 'html'
        with open(soup_path, 'r') as f:
            soup = bs4.BeautifulSoup(f, features='html.parser')
        data.append((soup, target))

    return data


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
    dataset = load_data('data')

    # test finding successful kernel function
    name_dataset = [(soup, target['name']) for soup, target in dataset]
    winners = find_successful_kernel_for_dataset(
        name_dataset, naive_traversal, naive_extract)
    rich.print("Dataset: " + ', '.join(target for _, target in name_dataset))

    rich.print("Winner kernels for duden attribute 'name' (tag name, attribute name): ", winners)

    kernel = winners[0]
    for soup, target in name_dataset:
        padded = (target + ':').ljust(16)
        attrval = naive_extract(soup, kernel)
        rich.print(f'{padded} <{kernel[0]} {kernel[1]}="{attrval}" />')
