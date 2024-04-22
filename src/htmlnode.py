class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ""
        html_string = ""
        for key, value in self.props.items():
            html_string += f' {key}="{value}"'
        return html_string

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, other):
        if isinstance(other, HTMLNode):
            return (
                self.tag == other.tag
                and self.value == other.value
                and self.children == other.children
                and self.children == other.children
            )
        return False


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("No value found in child LeafNode!")
        else:
            if self.tag is None:
                return self.value
            elif self.props is None:
                return f"<{self.tag}>{self.value}</{self.tag}>"
            else:
                return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag must be set for ParentNode!")
        if self.children is None:
            raise ValueError("ParentNode must have children!")

        child_html = ""
        for child in self.children:
            child_html += child.to_html()
        if self.props is not None:
            return f"<{self.tag}{self.props_to_html()}>{child_html}</{self.tag}>"
        else:
            return f"<{self.tag}>{child_html}</{self.tag}>"
