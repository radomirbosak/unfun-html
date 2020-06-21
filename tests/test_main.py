# -*- coding: utf-8 -*-
"""Test main module"""

import bs4

from unfun_html.main import function, naive_traversal


def test_function():
    """Test sample function"""
    function()


def test_naive_traversal_empty():
    """Test naive traversal with empty HTML"""
    html = ''
    soup = bs4.BeautifulSoup(html, features='html.parser')
    gen = naive_traversal(soup)
    assert list(gen) == []


def test_naive_traversal_noattrs():
    """Test naive traversal with single tag without attributes"""
    html = '<b>bold text</b><br />'
    soup = bs4.BeautifulSoup(html, features='html.parser')
    gen = naive_traversal(soup)
    assert list(gen) == []


def test_naive_traversal_single():
    """Test naive traversal with single tag without attributes"""
    html = '<font color="red">red text</font><br />'
    soup = bs4.BeautifulSoup(html, features='html.parser')
    gen = naive_traversal(soup)
    assert list(gen) == [('font', 'color')]


def test_naive_traversal_bad_nodes():
    """Test if bad tags are ignored"""
    html = '''<!DOCTYPE html>
    <a href="blab">link</a>
    <!-- some comment -->
    <script type="text/css">
        var i = 1;
    </script>'''
    soup = bs4.BeautifulSoup(html, features='html.parser')
    gen = naive_traversal(soup)
    assert list(gen) == [('a', 'href'), ('script', 'type')]


def test_naive_traversal_list_attrs():
    """Test if list-type attributes are included"""
    html = '''<nav rel="horse" />'''
    soup = bs4.BeautifulSoup(html, features='html.parser')
    gen = naive_traversal(soup)
    assert list(gen) == [('nav', 'rel')]
