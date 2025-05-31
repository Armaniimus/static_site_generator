import unittest

from blockconverter import markdown_to_blocks, block_to_block_type, BlockType


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
	
if __name__ == "__main__":
	unittest.main()