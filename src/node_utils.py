import re
from pathlib import Path
import os
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
from src.htmlnode import LeafNode, HTMLNode, ParentNode


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type not in TextTypes:
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
            continue
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


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def quote_block_to_html_node(block: str) -> HTMLNode:
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def ul_block_to_html_node(block: str) -> HTMLNode:
    return ParentNode(
        tag=HTMLTags.UNORDERED_LIST,
        children=[
            LeafNode(tag=HTMLTags.LIST_ITEM, value=line)
            for line in map(
                lambda x: x.lstrip("*").lstrip("-").lstrip(), block.split("\n")
            )
        ],
    )


def ol_block_to_html_node(block: str) -> HTMLNode:
    return ParentNode(
        tag=HTMLTags.ORDERED_LIST,
        children=[
            LeafNode(tag=HTMLTags.LIST_ITEM, value=line)
            for line in map(
                lambda x: re.sub(r"^[0-9]+\.\s", "", x).lstrip(), block.split("\n")
            )
        ],
    )


def code_block_to_html_node(block: str) -> HTMLNode:
    return ParentNode(
        tag=HTMLTags.PRE,
        children=[
            LeafNode(
                tag=HTMLTags.CODE,
                value=block.lstrip("```").rstrip("```").strip(),
            )
        ],
    )


def heading_block_to_html_node(block: str) -> HTMLNode:
    return ParentNode(
        tag=f"h{len(re.findall(MarkdownBlockRegexPattern.HEADING, block)[0]) - 1}",
        children=text_to_children(block.lstrip(MarkdownDelimiters.HEADING).lstrip()),
    )


def paragraph_block_to_html_node(block: str) -> HTMLNode:
    return LeafNode(
        tag=HTMLTags.PARAGRAPH,
        value=block,
    )


def block_to_html_node(block: str) -> HTMLNode:
    block_type = block_to_block_type(block)
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


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        children.append(block_to_html_node(block))

    return ParentNode(tag="div", children=children)


def extract_title(markdown: str) -> str:
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line.strip("# ")

    raise ValueError("Markdown has no h1 header!")


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    markdown_html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", markdown_html)
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template)


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str
) -> None:
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)
