import os
import shutil

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


def copy_contents_from(src: str, dst: str) -> None:
    if not os.path.exists(dst):
        os.mkdir(dst)

    for filename in os.listdir(src):
        src_path = os.path.join(src, filename)
        dst_path = os.path.join(dst, filename)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
        else:
            copy_contents_from(src_path, dst_path)


def main():
    copy_contents_from("static", "public")


main()
