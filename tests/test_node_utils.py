import unittest
from src.node_utils import split_nodes_delimiter
from src.constants import MarkdownDelimiters, TextTypes
from src.textnode import TextNode


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is text with a **bolded** word.", TextTypes.TEXT)

        expected_nodes = [
            TextNode("This is text with a ", TextTypes.TEXT),
            TextNode("bolded", TextTypes.BOLD),
            TextNode(" word.", TextTypes.TEXT),
        ]

        self.assertEqual(
            split_nodes_delimiter([node], MarkdownDelimiters.BOLD, TextTypes.BOLD),
            expected_nodes,
        )

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is text with a *italic* word.", TextTypes.TEXT)

        expected_nodes = [
            TextNode("This is text with a ", TextTypes.TEXT),
            TextNode("italic", TextTypes.ITALIC),
            TextNode(" word.", TextTypes.TEXT),
        ]

        self.assertEqual(
            split_nodes_delimiter([node], MarkdownDelimiters.ITALIC, TextTypes.ITALIC),
            expected_nodes,
        )

    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with `code` word.", TextTypes.TEXT)

        expected_nodes = [
            TextNode("This is text with ", TextTypes.TEXT),
            TextNode("code", TextTypes.CODE),
            TextNode(" word.", TextTypes.TEXT),
        ]

        self.assertEqual(
            split_nodes_delimiter([node], MarkdownDelimiters.CODE, TextTypes.CODE),
            expected_nodes,
        )

    def test_split_nodes_delimiter_beginning(self):
        node = TextNode("**Bold** is start of this sentence.", TextTypes.TEXT)

        expected_nodes = [
            TextNode("Bold", TextTypes.BOLD),
            TextNode(" is start of this sentence.", TextTypes.TEXT),
        ]

        self.assertEqual(
            split_nodes_delimiter([node], MarkdownDelimiters.BOLD, TextTypes.BOLD),
            expected_nodes,
        )

    def test_split_nodes_delimiter_end(self):
        node = TextNode("The end of this sentence is **bold**", TextTypes.TEXT)

        expected_nodes = [
            TextNode("The end of this sentence is ", TextTypes.TEXT),
            TextNode("bold", TextTypes.BOLD),
        ]

        self.assertEqual(
            split_nodes_delimiter([node], MarkdownDelimiters.BOLD, TextTypes.BOLD),
            expected_nodes,
        )


if __name__ == "__main__":
    unittest.main()
