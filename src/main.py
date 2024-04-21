from textnode import TextNode
from htmlnode import LeafNode
from constants import TextTypes, HTMLTags, HTMLProps, MarkdownDelimiters
from node_utils import split_nodes_delimiter


def main():
    textnode = TextNode("This is a text node.", "bold", "https://www.boot.dev")
    print(textnode)

    nodes = [TextNode("This node has **bold** text.", "text")]
    print(split_nodes_delimiter(old_nodes=nodes, delimiter=MarkdownDelimiters.BOLD, text_type=TextTypes.BOLD))
    


main()
