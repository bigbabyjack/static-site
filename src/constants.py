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


class HTMLProps(StrEnum):
    LINK = "href"
    IMAGE_SRC = "src"
    ALT_TEXT = "alt"


class MarkdownDelimiters(StrEnum):
    BOLD = "**"
    ITALIC = "*"
    CODE = "`"


class MarkdownBlockType(StrEnum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


class MarkdownBlockRegexPattern(StrEnum):
    HEADING = r"^#{1,6}$"
    CODE = r"^```$"
    QUOTE = r"^>$"
    UNORDERED_LIST = r"^[\*-]$"
    ORDERED_LIST = r"^1\.$"
