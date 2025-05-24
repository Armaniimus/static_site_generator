from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
	NORMAL = "normal"
	BOLD = "bold"
	ITALIC = "italic"
	CODE = "code"
	LINK = "link"
	IMAGE = "image"

class TextNode:
	def __init__(self, text, text_type, url = None):
		self.text = text
		self.text_type = text_type
		self.url = url
	
	def __eq__(self, other):
		if self.text != other.text:
			return False
		elif self.text_type != other.text_type:
			return False
		elif self.url != other.url:
			return False
		return True
	
	def __repr__(self):
		return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
	
	def to_html_node(self):
		if self.text_type == TextType.NORMAL:
			node = LeafNode(None, self.text)
		elif self.text_type == TextType.BOLD:
			node = LeafNode("b", self.text)
		elif self.text_type == TextType.ITALIC:
			node = LeafNode("i", self.text)
		elif self.text_type == TextType.CODE:
			node = LeafNode("code", self.text)
		elif self.text_type == TextType.LINK:
			node = LeafNode("a", self.text, {"href": self.url})
		elif self.text_type == TextType.IMAGE:
			node = LeafNode("img", None, {"alt": self.text, "src": self.url})

		return node