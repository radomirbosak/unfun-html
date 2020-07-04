# -*- coding: utf-8 -*-
"""Test main module"""
# pylint: disable=redefined-outer-name

import bs4

from unfun_html.main import (
    naive_traversal, naive_extract, find_successful_kernel)


def compile_soup(html):
    """Shorten BeautifulSoup constructor"""
    return bs4.BeautifulSoup(html, features='html.parser')


def test_naive_traversal_empty():
    """Test naive traversal with empty HTML"""
    html = ''
    gen = naive_traversal(compile_soup(html))
    assert list(gen) == []


def test_naive_traversal_noattrs():
    """Test naive traversal with single tag without attributes"""
    html = '<b>bold text</b><br />'
    gen = naive_traversal(compile_soup(html))
    assert list(gen) == []


def test_naive_traversal_single():
    """Test naive traversal with single tag without attributes"""
    html = '<font color="red">red text</font><br />'
    gen = naive_traversal(compile_soup(html))
    assert list(gen) == [('font', 'color')]


def test_naive_traversal_bad_nodes():
    """Test if bad tags are ignored"""
    html = '''<!DOCTYPE html>
    <a href="blab">link</a>
    <!-- some comment -->
    <script type="text/css">
        var i = 1;
    </script>'''
    gen = naive_traversal(compile_soup(html))
    assert list(gen) == [('a', 'href'), ('script', 'type')]


def test_naive_traversal_list_attrs():
    """Test if list-type attributes are included"""
    html = '''<nav rel="horse" />'''
    gen = naive_traversal(compile_soup(html))
    assert list(gen) == [('nav', 'rel')]


def test_naive_extract_empty():
    """Test empty soup finds no entry"""
    html = ''
    value = naive_extract(compile_soup(html), ('a', 'b'))
    assert value is None


def test_naive_extract_single():
    """Test single tag/attribute is extracted"""
    html = 'text<a href="example.com">link</a>end'
    value = naive_extract(compile_soup(html), ('a', 'href'))
    assert value == 'example.com'


def test_naive_extract_no_find_class():
    """Test single tag/attribute is extracted"""
    html = '<div class="pretty">content</div>'
    value = naive_extract(compile_soup(html), ('div', 'class'))
    assert value is None


def test_naive_extract_find_first():
    """Test single tag/attribute is extracted"""
    html = '<font color="red">a</font>b<font color="green">c</font>'
    value = naive_extract(compile_soup(html), ('font', 'color'))
    assert value == 'red'


def test_find_successful_kernel():
    """ Test that generator results that extract to target are returned"""
    # pylint: disable=multiple-statements
    def generator(soup): return range(soup)
    def extractor(soup, kernel): return kernel % 2  # pylint: disable=unused-argument
    target = 1
    soup = 5
    winners = find_successful_kernel(soup, generator, extractor, target)
    assert winners == [1, 3]
