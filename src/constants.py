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
    ITALICS = "*"
    CODE = "`"
