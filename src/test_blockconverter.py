import unittest

from blockconverter import *


class TestTextNodeToHtml(unittest.TestCase):
	def test_markdown_to_blocks(self):
		md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""

		blocks = markdown_to_blocks(md)


		self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

	def test_markdown_to_blocks_no_empty_lines(self):
		md = """
This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line 








- This is a list
- with items 




"""

		blocks = markdown_to_blocks(md)


		self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
	
	def test_block_to_block_type_heading_first(self):
		text = "# heading1"

		actual = block_to_block_type(text)

		self.assertEqual(BlockType.HEADING, actual)

	def test_block_to_block_type_heading_last(self):
		text = "###### heading6"

		actual = block_to_block_type(text)

		self.assertEqual(BlockType.HEADING, actual)

	def test_block_to_block_type_heading_all_cases(self):
		headings = [
			"# heading1",
    		"## heading2",
			"### heading3",
			"#### heading4",
			"##### heading5",
			"###### heading6"
		]

		for h in headings:
			actual = block_to_block_type(h)
			message = f"\ntest failed: actual is not equal to BlockType.HEADING\nactual == {actual}\ntestedString == {h}"
			self.assertEqual(BlockType.HEADING, actual, message)
	
	def test_block_to_block_type_heading_false_cases(self):
		headings = [
			"heading0",
			"#heading1",
    		"##heading2",
			"###heading3",
			"####heading4",
			"#####heading5",
			"######heading6",
			"####### heading7"
		]

		for h in headings:
			actual = block_to_block_type(h)
			message = f"\ntest failed: actual is not equal to BlockType.PARAGRAPH\nactual == {actual}\ntestedString == {h}"
			self.assertEqual(BlockType.PARAGRAPH, actual, message)

	def test_block_to_block_type_code(self):
		string = "``` ```"

		actual = block_to_block_type(string)
			
		self.assertEqual(BlockType.CODE, actual)

	def test_block_to_block_type_quote(self):
		string = """>1
> 2
> 3"""

		actual = block_to_block_type(string)
			
		self.assertEqual(BlockType.QUOTE, actual)

	def test_block_to_block_type_unordered_list(self):
		string = """- a
- b
- c"""

		actual = block_to_block_type(string)
			
		self.assertEqual(BlockType.UNORDERED_LIST, actual)

	def test_block_to_block_type_ordered_list(self):
		string = """1. a
2. b
3. c"""

		actual = block_to_block_type(string)
			
		self.assertEqual(BlockType.ORDERED_LIST, actual)

	def test_block_to_block_type_paragraph(self):
		paragraphs = [
			">",
			"-a",
			"-",
			"1.a",
			"1 a",
			"1.",
			"` ```",
			"`` ```",
			"``` ``",
			"``` `",
			"`` ``",
			"` ``",
			"`` `",
			"```"
		]

		for p in paragraphs:
			actual = block_to_block_type(p)
			message = f"\ntest failed: actual is not equal to BlockType.PARAGRAPH\nactual == {actual}\ntestedString == {p}"
			self.assertEqual(BlockType.PARAGRAPH, actual, message)

	def test_create_heading_block(self):
		#[inputdata, expected]
		inputs = [
			("# h1", LeafNode("h1", "h1")),
			("## h2", LeafNode("h2", "h2")),
			("### h3", LeafNode("h3", "h3")),
			("#### h4", LeafNode("h4", "h4")),
			("##### h5", LeafNode("h5", "h5")),
			("###### h6", LeafNode("h6", "h6"))
		]

		for i in inputs:
			actual = create_heading_block(i[0])
			message = f"\nFailed: \n\tinput={i[0]} \n\tactual={actual} \n\texpected={i[1]}"
			self.assertEqual(actual, i[1], message)

	def test_create_paragraph_block(self):
		input = "this is dummy test"
		expected = ParentNode("p", [LeafNode(None, "this is dummy test")])

		actual = create_paragraph_block(input)

		message = f"\nFailed: \n\tinput={input} \n\tactual={actual} \n\texpected={expected}"
		self.assertEqual(actual, expected, message)

	def test_create_paragraph_block_children(self):
		input = "this is **dummy** test"
		expected = ParentNode("p", [LeafNode(None, "this is "), LeafNode("b", "dummy"), LeafNode(None, " test")])

		actual = create_paragraph_block(input)

		message = f"\nFailed: \n\tinput={input} \n\tactual={actual} \n\texpected={expected}"
		self.assertEqual(actual, expected, message)
	
	def test_create_code_block(self):
		code_block_inside = """
		**bold**
		_italic_
		"""

		input = "```" + code_block_inside + "```"

		expected = ParentNode("pre", [LeafNode("code", code_block_inside)])

		actual = create_code_block(input)

		message = f"\nFailed: \n\tinput={input} \n\tactual={actual} \n\texpected={expected}"
		self.assertEqual(actual, expected, message)

	def test_create_quote_block(self):
		input = """> quote
> quote2
"""
		expected_text = """quote
quote2
"""
		expected = LeafNode("blockquote", expected_text)

		actual = create_quote_block(input)

		message = f"\nFailed: \n\tinput={input} \n\tactual={actual} \n\texpected={expected}"
		self.assertEqual(actual, expected, message)

	def test_create_unordered_list_block(self):
		input = """- ape
- whale
- giraffe
- dog"""
		actual = create_unordered_list_block(input)

		expected = ParentNode("ul", [
			LeafNode("li", "ape"),
			LeafNode("li", "whale"),
			LeafNode("li", "giraffe"),
			LeafNode("li", "dog")
		])

		message = f"\nFailed: \n\tinput={input} \n\tactual={actual} \n\texpected={expected}"
		self.assertEqual(actual, expected, message)

	def test_create_ordered_list_block(self):
		input = """1. ape
2. whale
3. giraffe
4. dog"""
		actual = create_ordered_list_block(input)

		expected = ParentNode("ol", [
			LeafNode("li", "ape"),
			LeafNode("li", "whale"),
			LeafNode("li", "giraffe"),
			LeafNode("li", "dog")
		])

		message = f"\nFailed: \n\tinput={input} \n\tactual={actual} \n\texpected={expected}"
		self.assertEqual(actual, expected, message)

	def test_create_ordered_list_block_long(self):
		count = 12

		input = ""
		for i in range(count):
			if (input != ""):
				input += "\n"
			input += f"{i}. item{i}"
		
		expected_list = []
		for i in range(count):
			expected_list.append(
				LeafNode("li", f"item{i}"),
			)

		expected = ParentNode("ol", expected_list)

		actual = create_ordered_list_block(input)

		message = f"\nFailed: \n\tinput={input} \n\tactual={actual} \n\texpected={expected}"
		self.assertEqual(actual, expected, message)

if __name__ == "__main__":
	unittest.main()