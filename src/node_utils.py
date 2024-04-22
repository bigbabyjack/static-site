import re
from typing import Tuple

from src.constants import (
    HTMLTags,
    HTMLProps,
    MarkdownBlockRegexPattern,
    TextTypes,
    MarkdownDelimiters,
    MarkdownBlockType,
)
from src.textnode import TextNode
from src.htmlnode import LeafNode, HTMLNode


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type in TextTypes:
        raise Exception(f"TextNode of type {text_node.text_type} is not valid.")

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
    else:
        return LeafNode(value=text_node.text)


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
                split_node_text = node.text.split(
                    f"![{image_tup[0]}]({image_tup[1]})", 1
                )
                if split_node_text[0] != "":
                    new_nodes.append(TextNode(split_node_text[0], TextTypes.TEXT))
                new_nodes.append(TextNode(image_tup[0], TextTypes.IMAGE, image_tup[1]))
                node.text = split_node_text[1]
            if node.text != "":
                new_nodes.append(TextNode(node.text, TextTypes.TEXT))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        extracted_links = extract_markdown_links(node.text)
        if len(extracted_links) == 0:
            new_nodes.append(node)
        else:
            for image_tup in extracted_links:
                split_node_text = node.text.split(
                    f"[{image_tup[0]}]({image_tup[1]})", 1
                )
                if split_node_text[0] != "":
                    new_nodes.append(TextNode(split_node_text[0], TextTypes.TEXT))
                new_nodes.append(TextNode(image_tup[0], TextTypes.LINK, image_tup[1]))
                node.text = split_node_text[1]
            if node.text != "":
                new_nodes.append(TextNode(node.text, TextTypes.TEXT))

    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    input_textnode = TextNode(text, TextTypes.TEXT)
    code_splits = split_nodes_delimiter(
        [input_textnode], MarkdownDelimiters.CODE, TextTypes.TEXT
    )
    bold_splits = split_nodes_delimiter(
        code_splits, MarkdownDelimiters.BOLD, TextTypes.TEXT
    )
    italic_splits = split_nodes_delimiter(
        bold_splits, MarkdownDelimiters.ITALIC, TextTypes.TEXT
    )
    image_splits = split_nodes_image(italic_splits)
    link_splits = split_nodes_link(image_splits)

    return link_splits


def markdown_to_blocks(text: str) -> list[str]:
    split_code_blocks = text.split("```")
    new_blocks = []
    for i, block in enumerate(split_code_blocks):
        if i % 2 == 1:
            new_blocks.append(f"```{block}```")
        else:
            new_blocks.extend(
                list(
                    filter(
                        lambda x: x != "",
                        map(lambda x: x.strip("\n").strip(), block.split("\n\n")),
                    )
                )
            )

    return new_blocks


# TODO: check if ordered_list numbers are valid
def block_to_block_type(block: str) -> str:
    # check for code block
    if block.startswith("```") and block.endswith("```"):
        return MarkdownBlockType.CODE
    else:
        if re.match(MarkdownBlockRegexPattern.HEADING, block):
            return MarkdownBlockType.HEADING
        elif re.match(MarkdownBlockRegexPattern.QUOTE, block):
            return MarkdownBlockType.QUOTE
        elif re.match(MarkdownBlockRegexPattern.UNORDERED_LIST, block):
            return MarkdownBlockType.UNORDERED_LIST
        elif re.match(MarkdownBlockRegexPattern.ORDERED_LIST, block):
            return MarkdownBlockType.ORDERED_LIST
        else:
            return MarkdownBlockType.PARAGRAPH


def quote_block_to_html_node(block: str) -> HTMLNode:
    return HTMLNode(
        tag=HTMLTags.BLOCKQUOTE,
        value="\n".join(map(lambda x: x.lstrip(">").lstrip(), block.split("\n"))),
    )


def ul_block_to_html_node(block: str) -> HTMLNode:
    return HTMLNode(
        tag=HTMLTags.UNORDERED_LIST,
        children=[
            HTMLNode(tag=HTMLTags.LIST_ITEM, value=line)
            for line in map(
                lambda x: x.lstrip("*").lstrip("-").lstrip(), block.split("\n")
            )
        ],
    )


def ol_block_to_html_node(block: str) -> HTMLNode:
    return HTMLNode(
        tag=HTMLTags.ORDERED_LIST,
        children=[
            HTMLNode(tag=HTMLTags.LIST_ITEM, value=line)
            for line in map(
                lambda x: re.sub(r"^[0-9]+\.\s", "", x).lstrip(), block.split("\n")
            )
        ],
    )


def code_block_to_html_node(block: str) -> HTMLNode:
    return HTMLNode(
        tag=HTMLTags.PRE,
        children=[
            HTMLNode(
                tag=HTMLTags.CODE,
                value=block.lstrip("```").rstrip("```").strip(),
            )
        ],
    )


def heading_block_to_html_node(block: str) -> HTMLNode:
    return HTMLNode(
        tag=f"h{len(re.findall(MarkdownBlockRegexPattern.HEADING, block)[0]) - 1}",
        value=block.lstrip(MarkdownDelimiters.HEADING).lstrip(),
    )


def paragraph_block_to_html_node(block: str) -> HTMLNode:
    return HTMLNode(
        tag=HTMLTags.PARAGRAPH,
        value=block,
    )


def block_to_html_node(block: str, block_type: str) -> HTMLNode:
    if block_type == MarkdownBlockType.QUOTE:
        return quote_block_to_html_node(block)
    if block_type == MarkdownBlockType.UNORDERED_LIST:
        return ul_block_to_html_node(block)
    if block_type == MarkdownBlockType.ORDERED_LIST:
        return ol_block_to_html_node(block)
    if block_type == MarkdownBlockType.CODE:
        return code_block_to_html_node(block)
    if block_type == MarkdownBlockType.HEADING:
        return heading_block_to_html_node(block)
    if block_type == MarkdownBlockType.PARAGRAPH:
        return paragraph_block_to_html_node(block)

    raise ValueError(f"Invalid block type {block_type}")


# TODO: Implement using helper functions
def markdown_to_html_node(markdown: str) -> HTMLNode:
    pass
