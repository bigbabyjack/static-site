from enum import StrEnum


class TextTypes(StrEnum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class HTMLTags(StrEnum):
    BOLD = "b"
    ITALIC = "i"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    HEADING_1 = "h1"
    HEADING_2 = "h2"
    HEADING_3 = "h3"
    HEADING_4 = "h4"
    HEADING_5 = "h5"
    HEADING_6 = "h6"
    DIV = "div"
    PARAGRAPH = "p"
    ORDERED_LIST = "ol"
    UNORDERED_LIST = "ul"
    LIST_ITEM = "li"
    PRE = "pre"
    BLOCKQUOTE = "blockquote"


class HTMLProps(StrEnum):
    LINK = "href"
    IMAGE_SRC = "src"
    ALT_TEXT = "alt"


class MarkdownDelimiters(StrEnum):
    BOLD = "**"
    ITALIC = "*"
    CODE = "`"
    HEADING = "#"


class MarkdownBlockType(StrEnum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


class MarkdownBlockRegexPattern(StrEnum):
    HEADING = r"^#{1,6}\s"
    CODE = r"^```$"
    QUOTE = r"^>\s"
    UNORDERED_LIST = r"^[\*-]\s"
    ORDERED_LIST = r"^1\.\s"
