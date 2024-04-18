from textnode import TextNode
from htmlnode import LeafNode
from constants import TextTypes, HTMLTags, HTMLProps


def text_node_to_html_node(text_node: TextNode):
    # VALID_TEXT_NODE_TYPES = [
    #     TextTypes.TEXT,
    #     TextTypes.BOLD,
    #     TextTypes.ITALIC,
    #     TextTypes.CODE,
    #     TextTypes.LINK,
    #     TextTypes.IMAGE,
    # ]

    if text_node.text_type in TextTypes:
        raise Exception(f"TextNode of type {text_node.text_type} is not valid.")

    if text_node.text_type == TextTypes.TEXT:
        return LeafNode(value=text_node.text)
    if text_node.text_type == TextTypes.BOLD:
        return LeafNode(tag=HTMLTags.BOLD, value=text_node.text)
    if text_node.text_type == TextTypes.ITALIC:
        return LeafNode(tag=HTMLTags.ITALIC, value=text_node.text)
    if text_node.text_type == TextTypes.CODE:
        return LeafNode(tag=HTMLTags.CODE, value=text_node.text)
    if text_node.text_type == TextTypes.LINK:
        return LeafNode(
            tag=HTMLTags.LINK,
            value=text_node.text,
            props={HTMLProps.LINK: text_node.url},
        )
    if text_node.text_type == TextTypes.IMAGE:
        return LeafNode(
            tag=HTMLTags.IMAGE,
            value=text_node.text,
            props={
                HTMLProps.IMAGE_SRC: text_node.url,
                HTMLProps.ALT_TEXT: text_node.text,
            },
        )


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type
) -> list[TextNode]:
    # new_nodes = []
    # for node in old_nodes:
    raise NotImplementedError("xD")


def main():
    textnode = TextNode("This is a text node.", "bold", "https://www.boot.dev")
    print(textnode)


main()
