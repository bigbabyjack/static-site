from src.textnode import TextNode
from src.htmlnode import LeafNode
from src.constants import TextTypes, HTMLTags, HTMLProps, MarkdownDelimiters
from src.node_utils import split_nodes_delimiter, split_nodes_image, text_to_textnodes


def main():
    text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"

    print(text_to_textnodes(text))


main()
