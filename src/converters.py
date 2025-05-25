from textnode import TextNode, TextType
from leafnode import LeafNode

def text_node_to_html_node(textnode):
	if textnode.text_type == TextType.TEXT:
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

def split_nodes_delimiter(old_nodes, delimiter, text_type):
	if not isinstance(old_nodes, list):
		raise ValueError("first argument[old_nodes] is not a list")
	if not isinstance(delimiter, str):
		raise ValueError("second argument[delimiter] is not a string")
	if not isinstance(text_type, TextType):
		raise ValueError("third argument[text_type] is not a TextType enum")

	nodes_out = []

	for node in old_nodes:
		split_func = get_split_node(delimiter, node.text_type, text_type)
		nodes_out += split_func(node.text)	
	return nodes_out

def get_split_node(delimiter, default_type, text_type):
	def splitNode(text):
		tmp_nodes = []
		split_str = text.split(delimiter, 2)
		if len(split_str) < 3:
			raise ValueError("splitting the string on {delimiter} resulted in less then 3 in the array therefore there must be an error in the delimitors in the source string")
		
		# add first node
		if len(split_str[0]) > 0: 
			tmp_nodes.append( TextNode(split_str[0], default_type) )
		
		# add second node
		tmp_nodes.append( TextNode(split_str[1], text_type) )
		
		# add third node
		if len(split_str[2]) > 0: 
			if delimiter in split_str[2]:
				tmp_nodes += splitNode(split_str[2])
			else:
				tmp_nodes.append( TextNode(split_str[2], default_type) )

		return tmp_nodes
	return splitNode