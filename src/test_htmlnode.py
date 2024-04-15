import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("div", "This is a div", [HTMLNode(
            "p", "This is a p")], {"class": "my-class"})
        self.assertEqual(
            repr(
                node), "HTMLNode(div, This is a div, [HTMLNode(p, This is a p, None, None)], {'class': 'my-class'})"
        )

    def test_repr_multiple_children(self):
        node = HTMLNode("div", "This is a div", [
                        HTMLNode("p", "This is a p"),
                        HTMLNode("p", "This is another p")], {"class": "my-class"})
        self.assertEqual(
            repr(
                node), "HTMLNode(div, This is a div, [HTMLNode(p, This is a p, None, None), HTMLNode(p, This is another p, None, None)], {'class': 'my-class'})"
        )

    def test_props_to_html(self):
        node = HTMLNode("div", "This is a div", None, {"class": "my-class"})
        self.assertEqual(node.props_to_html(), ' class="my-class"')


if __name__ == "__main__":
    unittest.main()
