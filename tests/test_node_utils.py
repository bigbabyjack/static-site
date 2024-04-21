import unittest
from src.node_utils import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
)
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


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"

        self.assertEqual(
            extract_markdown_images(text),
            [
                (
                    "image",
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                ),
                (
                    "another",
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png",
                ),
            ],
        )

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"

        self.assertEqual(
            extract_markdown_links(text),
            [
                ("link", "https://www.example.com"),
                ("another", "https://www.example.com/another"),
            ],
        )


class TestExtractMarkdownLinks(unittest.TestCase):
    pass


if __name__ == "__main__":
    unittest.main()
