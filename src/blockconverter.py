from enum import Enum
import re
from converters import text_to_textnodes, text_node_to_html_node
from parentnode import ParentNode
from leafnode import LeafNode

class BlockType(Enum):
	PARAGRAPH = "paragraph"
	HEADING = "heading"
	CODE = "code"
	QUOTE = "quote"
	UNORDERED_LIST = "unordered_list"
	ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
	blocks = markdown.split("\n\n")

	for key in range(len(blocks)):
		blocks[key] = blocks[key].strip().strip("\n").replace(' \n','\n')

	func = lambda block: block != ""
	filtered_blocks = list( filter(func, blocks) )
	
	return filtered_blocks

def block_to_block_type(block):
	is_heading = re.match(r"^[#]{1,6} \S", block) != None
	is_code = re.fullmatch(r"^```[\s\S]+```$", block) != None
	is_quote_regex = r"^>[\s\S]+"
	is_unordered_list_regex = r"^- [\s\S]+"
	is_ordered_list_regex = r"^[0-9]+\. [\s\S]+"

	if is_heading:
		return BlockType.HEADING
	
	elif is_code:
		return BlockType.CODE
	else:
		def checker(regex):
			lines = block.split("\n")
			for l in lines:
				if re.fullmatch(regex, l) == None:
					return False
				
			return True
		
		is_quote = checker(is_quote_regex)
		is_unordered_list = checker(is_unordered_list_regex)
		is_ordered_list = checker(is_ordered_list_regex)

		if is_quote:
			return BlockType.QUOTE
		elif is_unordered_list:
			return BlockType.UNORDERED_LIST
		elif is_ordered_list:
			return BlockType.ORDERED_LIST
	
	return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
	blocks = markdown_to_blocks(markdown)

	nodes = []

	for b in blocks:
		nodes.append(create_html_node_from_block(b))

	return ParentNode("div", nodes)

def create_html_node_from_block(block):
	block_type = block_to_block_type(block)

	if block_type == BlockType.PARAGRAPH:
		return create_paragraph_block(block)
	
	if block_type == BlockType.HEADING:
		return create_heading_block(block)
	
	if block_type == BlockType.CODE:
		return create_code_block(block)
	
	if block_type == BlockType.ORDERED_LIST:
		return create_ordered_list_block(block)
	
	if block_type == BlockType.UNORDERED_LIST:
		return create_unordered_list_block(block)
	
	if block_type == BlockType.QUOTE:
		return create_quote_block(block)
	
	raise ValueError("given block has no valid block-type")

def create_ordered_list_block(text):
	lines = text.split("\n")
	children = []
	for l in lines:
		children.append(
			LeafNode("li", l.lstrip("1234567890.").lstrip(" "))
		)

	return ParentNode("ol", children)

def create_unordered_list_block(text):
	lines = text.split("\n")
	children = []
	for l in lines:
		children.append(
			LeafNode("li", l.lstrip("-").lstrip(" "))
		)

	return ParentNode("ul", children)

def create_quote_block(text):
	lines = text.split("\n")
	quote_text = ""
	for l in lines:
		if (quote_text != ""):
			quote_text += "\n"
		quote_text += l.lstrip("> ")

	return LeafNode("blockquote", quote_text)

def create_code_block(text):
	text_code = text.replace("```", "").strip(" \n\t")

	return ParentNode("pre", [LeafNode("code", text_code)])

def create_paragraph_block(text):
	text_nodes = text_to_textnodes(text)
	leaf_nodes = []
	for n in text_nodes:

		html_node = text_node_to_html_node(n)
		if (html_node.value != None):
			html_node.value = html_node.value.replace("\n", " ")
		leaf_nodes.append(html_node)

	return ParentNode("p", leaf_nodes)

def create_heading_block(text):
	if text.startswith("######"):
		node_lvl = "h6"
	elif text.startswith("#####"):
		node_lvl = "h5"
	elif text.startswith("####"):
		node_lvl = "h4"
	elif text.startswith("###"):
		node_lvl = "h3"
	elif text.startswith("##"):
		node_lvl = "h2"
	elif text.startswith("#"):
		node_lvl = "h1"
	
	filtered_text = text.lstrip("# ")

	return LeafNode(node_lvl, filtered_text)