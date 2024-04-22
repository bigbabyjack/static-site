from src.textnode import TextNode
from src.htmlnode import LeafNode
from src.constants import TextTypes, HTMLTags, HTMLProps, MarkdownDelimiters
from src.node_utils import (
    ol_block_to_html_node,
    split_nodes_delimiter,
    split_nodes_image,
    text_to_textnodes,
    markdown_to_blocks,
)


def main():
    text = "1. this is an ordered list\n2. you can tell by how it is\n3. isn't that cool"
    print(ol_block_to_html_node(text))


main()
