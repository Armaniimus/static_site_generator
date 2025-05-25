from textnode import TextType
from leafnode import LeafNode

def text_node_to_html_node(textnode):
	if textnode.text_type == TextType.NORMAL:
		node = LeafNode(None, textnode.text)
	elif textnode.text_type == TextType.BOLD:
		node = LeafNode("b", textnode.text)
	elif textnode.text_type == TextType.ITALIC:
		node = LeafNode("i", textnode.text)
	elif textnode.text_type == TextType.CODE:
		node = LeafNode("code", textnode.text)
	elif textnode.text_type == TextType.LINK:
		node = LeafNode("a", textnode.text, {"href": textnode.url})
	elif textnode.text_type == TextType.IMAGE:
		node = LeafNode("img", None, {"alt": textnode.text, "src": textnode.url})

	return node