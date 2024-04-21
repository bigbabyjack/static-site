import re
from typing import Tuple

from src.constants import HTMLTags, HTMLProps, TextTypes, MarkdownDelimiters
from src.textnode import TextNode
from src.htmlnode import LeafNode


def text_node_to_html_node(text_node: TextNode):
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
    old_nodes: list[TextNode], delimiter: str, text_type: str
) -> list[TextNode]:
    if text_type not in TextTypes:
        raise ValueError(f"Invalid text type: {text_type}")
    if delimiter not in MarkdownDelimiters:
        raise ValueError(f"Invalid markdown delimiter: {delimiter}")

    DELIMITER_TO_TEXT_TYPE = {
        "**": TextTypes.BOLD,
        "*": TextTypes.ITALIC,
        "`": TextTypes.CODE,
    }

    new_nodes: list[TextNode] = []
    # iterate through each node
    for old_node in old_nodes:
        # if the node is not a text node, add as is
        if old_node.text_type != TextTypes.TEXT:
            new_nodes.append(old_node)
        # if we have a text node
        else:
            # split the node text
            split_old_node_text = old_node.text.split(delimiter)
            # check for invalid markdown format
            if len(split_old_node_text) % 2 == 0:
                raise ValueError("Invalid markdown syntax: Missing closing delimiter.")
            for i, text in enumerate(split_old_node_text):
                # only consider nonempty strings
                if text == "":
                    continue
                # only odd indices will contain the new Node type
                if i % 2 == 0:
                    # make sure it isn't the empty string
                    new_nodes.append(TextNode(text=text, text_type=TextTypes.TEXT))
                else:
                    new_nodes.append(
                        TextNode(text=text, text_type=DELIMITER_TO_TEXT_TYPE[delimiter])
                    )

    return new_nodes


def extract_markdown_images(text: str) -> list[Tuple[str, str]]:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text: str) -> list[Tuple[str, str]]:
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        extracted_images = extract_markdown_images(node.text)
        if len(extracted_images) == 0:
            new_nodes.append(node)
        else:
            for image_tup in extracted_images:
                split_node_text = node.text.split(f"![{image_tup[0]}]({image_tup[1]})")
                if split_node_text[0] != "":
                    new_nodes.append(TextNode(split_node_text[0], TextTypes.TEXT))
                new_nodes.append(TextNode(image_tup[0], TextTypes.IMAGE, image_tup[1]))
                node.text = split_node_text[1]

    return new_nodes


# TODO: Implement function
def split_nodes_link(old_nodes):
    pass
