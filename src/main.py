from textnode import TextNode
from htmlnode import LeafNode
from constants import TextTypes, HTMLTags, HTMLProps, MarkdownDelimiters
from node_utils import split_nodes_delimiter, split_nodes_image


def main():
    node = TextNode(
        "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
        TextTypes.TEXT,
    )

    print(split_nodes_image([node]))


main()
