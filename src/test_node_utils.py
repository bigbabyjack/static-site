import unittest
from src.node_utils import split_nodes_delimiter
from src.constants import MarkdownDelimiters, TextTypes
from src.textnode import TextNode


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a **bolded** word.", TextTypes.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], MarkdownDelimiters.BOLD, TextTypes.BOLD),
            '[TextNode("This is text with a ", "text"), TextNode("bolded", "bold"), TextNode(" word.", "text")]',
        )


if __name__ == "__main__":
    unittest.main()
