import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode(
            "div",
            "This is a div",
            [HTMLNode("p", "This is a p")],
            {"class": "my-class"},
        )
        self.assertEqual(
            repr(node),
            "HTMLNode(div, This is a div, [HTMLNode(p, This is a p, None, None)], {'class': 'my-class'})",
        )

    def test_repr_multiple_children(self):
        node = HTMLNode(
            "div",
            "This is a div",
            [HTMLNode("p", "This is a p"), HTMLNode("p", "This is another p")],
            {"class": "my-class"},
        )
        self.assertEqual(
            repr(node),
            "HTMLNode(div, This is a div, [HTMLNode(p, This is a p, None, None), HTMLNode(p, This is another p, None, None)], {'class': 'my-class'})",
        )

    def test_props_to_html(self):
        node = HTMLNode("div", "This is a div", None, {"class": "my-class"})
        self.assertEqual(node.props_to_html(), ' class="my-class"')


class TestLeafNode(unittest.TestCase):
    def test_to_html_p(self):
        p_node = LeafNode("p", "This is a leaf node.")

        self.assertEqual(p_node.to_html(), "<p>This is a leaf node.</p>")

    def test_to_html_link(self):
        link_node = LeafNode("a", "This is a link node.", {"href": "github.com"})
        self.assertEqual(
            link_node.to_html(), '<a href="github.com">This is a link node.</a>'
        )


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_attr(self):
        node = ParentNode(
            "div",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            {"class_": "my-class"},
        )

        self.assertEqual(
            node.to_html(),
            '<div class_="my-class"><b>Bold text</b>Normal text<i>italic text</i>Normal text</div>',
        )

    def test_to_html_nested_children(self):
        node = ParentNode(
            "div",
            [
                ParentNode("p", [LeafNode("b", "Bold text")]),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            {"class_": "my-class"},
        )

        self.assertEqual(
            node.to_html(),
            '<div class_="my-class"><p><b>Bold text</b></p><i>italic text</i>Normal text</div>',
        )


if __name__ == "__main__":
    unittest.main()
