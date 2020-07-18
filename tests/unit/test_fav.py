"""
Test FirstAttributeValue generator-extractor
"""

# pylint: disable=redefined-outer-name
import bs4
from pytest import fixture, raises

from unfun_html.gentor import FirstAttributeValueGentor, CannotExtractKernel


def soup_compile(html):
    """Cook soup"""
    return bs4.BeautifulSoup(html, features='html.parser')


@fixture
def fav():
    """Shortcut for fav gentor"""
    return FirstAttributeValueGentor()


def test_fav_extract(fav):
    """Simple extract test"""
    soup = soup_compile('<a href="1">A</a><a href="2">B</a>')
    assert fav.extract(soup, ('a', 'href')) == '1'


def test_fav_traverse(fav):
    """Simple traverse test"""
    soup = soup_compile(
        '<!DOCTYPE html><a href="1">A</a>'
        '<div class="baby">B</div><!-- comment -->')
    kernels = list(fav.traverse(soup))

    assert len(kernels) == 2
    assert ('a', 'href') in kernels
    assert ('div', 'class') in kernels


def test_fav_semiwinners(fav):
    """Check for semiwinners"""
    soup = soup_compile('<a href="2" /><a href="1" /><b href="1" /><font color="1">1</font>')
    result = list(fav.semiwinners(soup, '1'))
    assert result == [('b', 'href'), ('font', 'color')]


def test_fav_winners(fav):
    """Check for winners"""
    soup = soup_compile('<a b="1" /><b c="1" /><d e="2" />')
    soup2 = soup_compile('<a b="2" /><b c="1" /><d e="1" />')
    dataset = [(soup, '1'), (soup2, '1')]
    result = list(fav.winners(dataset))
    assert result == [('b', 'c')]


def test_naive_traversal_empty(fav):
    """Test naive traversal with empty HTML"""
    html = ''
    gen = fav.traverse(soup_compile(html))
    assert list(gen) == []


def test_naive_traversal_noattrs(fav):
    """Test naive traversal with single tag without attributes"""
    html = '<b>bold text</b><br />'
    gen = fav.traverse(soup_compile(html))
    assert list(gen) == []


def test_naive_traversal_single(fav):
    """Test naive traversal with single tag without attributes"""
    html = '<font color="red">red text</font><br />'
    gen = fav.traverse(soup_compile(html))
    assert list(gen) == [('font', 'color')]


def test_naive_traversal_bad_nodes(fav):
    """Test if bad tags are ignored"""
    html = '''<!DOCTYPE html>
    <a href="blab">link</a>
    <!-- some comment -->
    <script type="text/css">
        var i = 1;
    </script>'''
    gen = fav.traverse(soup_compile(html))
    assert list(gen) == [('a', 'href'), ('script', 'type')]


def test_naive_traversal_list_attrs(fav):
    """Test if list-type attributes are included"""
    html = '''<nav rel="horse" />'''
    gen = fav.traverse(soup_compile(html))
    assert list(gen) == [('nav', 'rel')]


def test_naive_extract_empty(fav):
    """Test empty soup finds no entry"""
    html = ''
    with raises(CannotExtractKernel):
        fav.extract(soup_compile(html), ('a', 'b'))


def test_naive_extract_single(fav):
    """Test single tag/attribute is extracted"""
    html = 'text<a href="example.com">link</a>end'
    value = fav.extract(soup_compile(html), ('a', 'href'))
    assert value == 'example.com'


def test_naive_extract_no_find_class(fav):
    """Test single tag/attribute is extracted"""
    html = '<div class="pretty">content</div>'
    with raises(CannotExtractKernel):
        fav.extract(soup_compile(html), ('div', 'class'))


def test_naive_extract_find_first(fav):
    """Test single tag/attribute is extracted"""
    html = '<font color="red">a</font>b<font color="green">c</font>'
    value = fav.extract(soup_compile(html), ('font', 'color'))
    assert value == 'red'
