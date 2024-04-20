from textnode import TextNode
from htmlnode import LeafNode
from constants import TextTypes, HTMLTags, HTMLProps, MarkdownDelimiters


def main():
    textnode = TextNode("This is a text node.", "bold", "https://www.boot.dev")
    print(textnode)


main()
