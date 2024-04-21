from src.textnode import TextNode
from src.htmlnode import LeafNode
from src.constants import TextTypes, HTMLTags, HTMLProps, MarkdownDelimiters
from src.node_utils import (
    split_nodes_delimiter,
    split_nodes_image,
    text_to_textnodes,
    markdown_to_blocks,
)


def main():
    text = """\n\n\n# This is a heading\n\n\n\n\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n\n\n\n* This is a list item\n* This is another list item"""
    print(markdown_to_blocks(text))


main()
