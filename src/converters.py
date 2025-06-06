from textnode import TextNode, TextType
from leafnode import LeafNode
import re

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
	elif textnode == None:
		raise Exception("textnode == None")
	else:
		raise Exception("invalid node given")

	return node

def split_nodes_italic(old_nodes):
	nodes_out = []

	for node in old_nodes:
		split_func = get_split_node("_", node.text_type, TextType.ITALIC)
		nodes_out += split_func(node)	
	return nodes_out

def split_nodes_bold(old_nodes):
	nodes_out = []

	for node in old_nodes:
		split_func = get_split_node("**", node.text_type, TextType.BOLD)
		nodes_out += split_func(node)	
	return nodes_out

def split_nodes_code(old_nodes):
	nodes_out = []

	for node in old_nodes:
		split_func = get_split_node("`", node.text_type, TextType.CODE)
		nodes_out += split_func(node)	
	return nodes_out

def get_split_node(delimiter, default_type, text_type):
	if not isinstance(delimiter, str):
		raise ValueError("second argument[delimiter] is not a string")
	if not isinstance(text_type, TextType):
		raise ValueError("third argument[text_type] is not a TextType enum")
	
	def splitNode(node):
		if node.text_type == TextType.IMAGE or node.text_type == TextType.LINK:
			return [node]
		
		text = node.text
		if text == "" or None:
			return []

		tmp_nodes = []
		split_str = text.split(delimiter, 2)
		if len(split_str) == 1:
			return [ TextNode(split_str[0], default_type) ]
		
		elif len(split_str) < 3:
			raise ValueError(f"splitting the string on {delimiter} resulted in less then 3 in the array therefore there must be an error in the delimitors in the source string\n\nsplit_str: {split_str}")
	
		# add first node
		if len(split_str[0]) > 0: 
			tmp_nodes.append( TextNode(split_str[0], default_type) )
		
		# add second node
		tmp_nodes.append( TextNode(split_str[1], text_type) )
		
		# add third node
		if len(split_str[2]) > 0: 
			if delimiter in split_str[2]:
				tmp_nodes += splitNode(TextNode(split_str[2], text_type))
			else:
				tmp_nodes.append( TextNode(split_str[2], default_type) )

		return tmp_nodes
	return splitNode

def extract_markdown_images(text):
	regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
	return re.findall(regex, text)

def extract_markdown_links(text):
	regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
	return re.findall(regex, text)

def __split_nodes_img_link(extract_func, remake_func, type):
	def inner_func(old_nodes):
		if not isinstance(old_nodes, list):
			raise ValueError("first argument[old_nodes] is not a list")
		
		nodes_out = []

		for node in old_nodes:
			if (node.text_type == TextType.IMAGE or node.text_type == TextType.LINK):
				nodes_out.append(node)
				continue
			
			base_text = node.text
			extracted_images = extract_func(node.text)

			if (len(extracted_images) == 0):
				nodes_out.append(node)
				continue			

			for i in range(len(extracted_images)):
				delimitor = remake_func(extracted_images[i])
				split_str = base_text.split(delimitor, 2)
				nodes_out.append( TextNode(split_str[0], node.text_type) )
				nodes_out.append( TextNode(extracted_images[i][0], type, extracted_images[i][1]) )
				base_text = split_str[1]
			if base_text != "" and len(extracted_images) > 0:
				nodes_out.append( TextNode(split_str[1], node.text_type) )
		return nodes_out
	return inner_func

def split_nodes_link(old_nodes):
	def remake_link(tuple):
		return f"[{tuple[0]}]({tuple[1]})"
	
	func = __split_nodes_img_link(extract_markdown_links, remake_link, TextType.LINK)
	
	return func(old_nodes)

def split_nodes_image(old_nodes):
	def remake_image(tuple):
		return f"![{tuple[0]}]({tuple[1]})"
	
	func = __split_nodes_img_link(extract_markdown_images, remake_image, TextType.IMAGE)

	return func(old_nodes)

def text_to_textnodes(text):
	stage0_nodes = [TextNode(text, TextType.TEXT)]
	stage1_nodes = split_nodes_image(stage0_nodes)
	stage2_nodes = split_nodes_link(stage1_nodes)
	
	stage3_nodes = split_nodes_bold(stage2_nodes)
	stage4_nodes = split_nodes_code(stage3_nodes)
	stage5_nodes = split_nodes_italic(stage4_nodes)

	return stage5_nodes