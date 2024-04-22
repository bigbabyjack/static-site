import unittest
from src.node_utils import (
    block_to_block_type,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks,
)
from src.constants import MarkdownBlockType, MarkdownDelimiters, TextTypes
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


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"

        self.assertEqual(
            extract_markdown_links(text),
            [
                ("link", "https://www.example.com"),
                ("another", "https://www.example.com/another"),
            ],
        )


class TestSplitNodesImage(unittest.TestCase):
    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            TextTypes.TEXT,
        )

        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("This is text with an ", TextTypes.TEXT),
                TextNode(
                    "image",
                    TextTypes.IMAGE,
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                ),
                TextNode(" and another ", TextTypes.TEXT),
                TextNode(
                    "second image",
                    TextTypes.IMAGE,
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
                ),
            ],
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with an [link](https://www.example.com/text) and another [second link](https://example.com/example) and here is more text.",
            TextTypes.TEXT,
        )

        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("This is text with an ", TextTypes.TEXT),
                TextNode(
                    "link",
                    TextTypes.LINK,
                    "https://www.example.com/text",
                ),
                TextNode(" and another ", TextTypes.TEXT),
                TextNode(
                    "second link",
                    TextTypes.LINK,
                    "https://example.com/example",
                ),
                TextNode(" and here is more text.", TextTypes.TEXT),
            ],
        )


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"

        self.assertEqual(
            text_to_textnodes(text),
            [
                TextNode("This is ", TextTypes.TEXT),
                TextNode("text", TextTypes.BOLD),
                TextNode(" with an ", TextTypes.TEXT),
                TextNode("italic", TextTypes.ITALIC),
                TextNode(" word and a ", TextTypes.TEXT),
                TextNode("code block", TextTypes.CODE),
                TextNode(" and an ", TextTypes.TEXT),
                TextNode(
                    "image",
                    TextTypes.IMAGE,
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                ),
                TextNode(" and a ", TextTypes.TEXT),
                TextNode("link", TextTypes.LINK, "https://boot.dev"),
            ],
        )


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        text = """# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is a list item\n* This is another list item"""
        self.assertEqual(
            markdown_to_blocks(text),
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is a list item\n* This is another list item",
            ],
        )

    def test_markdown_to_blocks_extra_lines(self):
        text = """\n\n\n# This is a heading\n\n\n\n\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n\n\n\n* This is a list item\n* This is another list item"""
        self.assertEqual(
            markdown_to_blocks(text),
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is a list item\n* This is another list item",
            ],
        )

    def test_markdown_to_blocks_code(self):
        text = "This is a paragraph\n\n# here is a heading\n\n```\nThis is some example code\n```\n\n and here is more paragraph\n\n* this is a list item\n* and another list item"
        self.assertEqual(
            markdown_to_blocks(text),
            [
                "This is a paragraph",
                "# here is a heading",
                "```\nThis is some example code\n```",
                "and here is more paragraph",
                "* this is a list item\n* and another list item",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type(self):
        block = "# This is a heading"

        self.assertEqual(
            block_to_block_type(block),
            MarkdownBlockType.HEADING,
        )

    def test_block_to_block_type_invalid(self):
        block = "#this is not a heading"

        self.assertEqual(block_to_block_type(block), MarkdownBlockType.PARAGRAPH)

    def test_block_to_block_type_code(self):
        block = "```\nthis is a code block\n```"

        self.assertEqual(block_to_block_type(block), MarkdownBlockType.CODE)


if __name__ == "__main__":
    unittest.main()
