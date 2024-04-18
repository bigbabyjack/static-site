from textnode import TextNode
from htmlnode import LeafNode


def text_node_to_html_node(text_node: TextNode):
    VALID_TEXT_NODE_TYPES = ["text", "bold", "italic", "code", "link", "image"]

    if text_node.text_type not in VALID_TEXT_NODE_TYPES:
        raise Exception(f"TextNode of type {text_node.text_type} is not valid.")

    if text_node.text_type == "text":
        return LeafNode(value=text_node.text)
    if text_node.text_type == "bold":
        return LeafNode(tag="b", value=text_node.text)
    if text_node.text_type == "italic":
        return LeafNode(tag="i", value=text_node.text)
    if text_node.text_type == "code":
        return LeafNode(tag="code", value=text_node.text)
    if text_node.text_type == "link":
        return LeafNode(
            tag="a",
            value=text_node.text,
            props={"href": text_node.url},
        )
    if text_node.text_type == "image":
        return LeafNode(
            tag="img",
            value=text_node.text,
            props={"src": text_node.url, "alt": text_node.text},
        )


def main():
    textnode = TextNode("This is a text node.", "bold", "https://www.boot.dev")
    print(textnode)


main()
