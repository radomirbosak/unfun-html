"""
Gentor which generates only tag attribute values. Ignores multiple-value attributes,
such as "class"

Currently duden word attributes have these types:

    | -------- | ----------------------------------------------------------------- |
    | str      | name, urlname, title, article, part_of_speech, origin, usage      |
    | int      | frequency                                                         |
    | list     | word_separation, grammar_raw, synonyms, words_before, words_after |
    | dict     | compounds                                                         |
    | list/str | meaning_overview                                                  |

From these:

FAV can extract:    name, urlname
FAV cannot extract: title, article, part_of_speech, origin, usage
"""

import bs4

from .gentor import Gentor, CannotExtractKernel


class FirstAttributeValueGentor(Gentor):
    """
    Gentor which generates only tag attribute values. Ignores multiple-value attributes,
    such as "class"
    """

    def traverse(self, soup):
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

    def extract(self, soup, kernel):
        """Evaluate (tag/attr tuples)"""
        node_name, attr_name = kernel

        node = soup.find(lambda node: node_has_attribute_nolist(node, node_name, attr_name))
        if node is None:
            raise CannotExtractKernel
        return node.attrs[attr_name]


def node_has_attribute_nolist(node, tag_name, attr_name):
    """
    Test if not has tag name `tag_name` and contains attribute `attr_name`
    """
    return \
        node.name == tag_name and \
        attr_name in node.attrs and \
        not isinstance(node.attrs.get(attr_name), list)
