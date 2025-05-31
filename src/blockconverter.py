from enum import Enum
import re

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