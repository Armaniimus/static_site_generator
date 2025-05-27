import unittest

from textnode import TextNode, TextType
from converters import *


class TestTextNodeToHtml(unittest.TestCase):
	def test_text(self):
		node = TextNode("This is a text node", TextType.TEXT)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, None)
		self.assertEqual(html_node.value, "This is a text node")
	
	def test_bold(self):
		node = TextNode("This is a text node", TextType.BOLD)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "b")
		self.assertEqual(html_node.value, "This is a text node")
	
	def test_italic(self):
		node = TextNode("This is a text node", TextType.ITALIC)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "i")
		self.assertEqual(html_node.value, "This is a text node")

	def test_code(self):
		node = TextNode("This is a text node", TextType.CODE)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "code")
		self.assertEqual(html_node.value, "This is a text node")
	
	def test_link(self):
		node = TextNode("This is a text node", TextType.LINK, "http://abc.com")
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "a")
		self.assertEqual(html_node.value, "This is a text node")
		self.assertEqual(html_node.props, {"href": "http://abc.com"})

	def test_image(self):
		node = TextNode("This is a text node", TextType.IMAGE, "http://abc.jpg")
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "img")
		self.assertEqual(html_node.value, None)
		self.assertEqual(html_node.props, {"alt": "This is a text node", "src": "http://abc.jpg"})

class TestSplitNodesDelimiter(unittest.TestCase):
	def test_split_nodes_delimiter_is_list(self):
		node = TextNode("This is text with a `code block` word", TextType.TEXT)
		actual_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

		self.assertEqual(isinstance(actual_nodes, list), True)
	
	def test_split_nodes_delimiter_runs_empty(self):
		actual_nodes = split_nodes_delimiter([], "`", TextType.CODE)

		self.assertEqual(isinstance(actual_nodes, list), True)
		self.assertEqual(actual_nodes, [])

	def test_split_nodes_delimiter_code_block(self):
		node = TextNode("This is text with a `code block` word", TextType.TEXT)
		expected_nodes = [
			TextNode("This is text with a ", TextType.TEXT),
			TextNode("code block", TextType.CODE),
			TextNode(" word", TextType.TEXT),
		]
		
		actual_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

		self.assertEqual(actual_nodes, expected_nodes)

	def test_split_nodes_delimiter_code_block_x2(self):
		node = TextNode("This is text with a `code block` word and `another code block` word", TextType.TEXT)
		expected_nodes = [
			TextNode("This is text with a ", TextType.TEXT),
			TextNode("code block", TextType.CODE),
			TextNode(" word and ", TextType.TEXT),
			TextNode("another code block", TextType.CODE),
			TextNode(" word", TextType.TEXT)
		]
		
		actual_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

		self.assertEqual(actual_nodes, expected_nodes)

	def test_split_nodes_delimiter_no_end(self):
		node = TextNode("This is text with a `code block`", TextType.TEXT)
		expected_nodes = [
			TextNode("This is text with a ", TextType.TEXT),
			TextNode("code block", TextType.CODE),
		]
		
		actual_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

		self.assertEqual(actual_nodes, expected_nodes)

	def test_split_nodes_delimiter_no_start(self):
		node = TextNode("`code block` word", TextType.TEXT)
		expected_nodes = [
			TextNode("code block", TextType.CODE),
			TextNode(" word", TextType.TEXT),
		]
		
		actual_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

		self.assertEqual(actual_nodes, expected_nodes)

	def test_split_nodes_delimiter_bold(self):
		node = TextNode("This is text with a **bold word** word", TextType.TEXT)
		expected_nodes = [
			TextNode("This is text with a ", TextType.TEXT),
			TextNode("bold word", TextType.BOLD),
			TextNode(" word", TextType.TEXT),
		]
		
		actual_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

		self.assertEqual(actual_nodes, expected_nodes)

	def test_split_nodes_delimiter_italic(self):
		node = TextNode("This is text with a _italic word_ word", TextType.TEXT)
		expected_nodes = [
			TextNode("This is text with a ", TextType.TEXT),
			TextNode("italic word", TextType.ITALIC),
			TextNode(" word", TextType.TEXT),
		]
		
		actual_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)

		self.assertEqual(actual_nodes, expected_nodes)

	def test_extract_markdown_images(self):
		matches = extract_markdown_images(
			"This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
		)
		self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
	
	def test_extract_markdown_images_alt_text(self):
		matches = extract_markdown_images(
			"This is text with an ![alternative_img_text](https://i.imgur.com/zjjcJKZ.png)"
		)
		self.assertListEqual([("alternative_img_text", "https://i.imgur.com/zjjcJKZ.png")], matches)

	def test_extract_markdown_images_x3(self):
		matches = extract_markdown_images(
			"This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)\n" +
			"This is another text with an ![fotoshoot](https://i.imgur.com/aob.png)\n" +
			"This is last text with an ![chores](https://i.imgur.com/deac.png)"
		)
		self.assertListEqual([
			("image", "https://i.imgur.com/zjjcJKZ.png"), 
			("fotoshoot", "https://i.imgur.com/aob.png"), 
			("chores", "https://i.imgur.com/deac.png") 
		], matches)

	def test_extract_markdown_links(self):
		matches = extract_markdown_links(
			"This is text with an [link](https://i.imgur.com)"
		)
		self.assertListEqual([("link", "https://i.imgur.com")], matches)

	def test_extract_markdown_links_alt_text(self):
		matches = extract_markdown_links(
			"This is text with an [alternative_link_text](https://i.imgur.com)"
		)
		self.assertListEqual([("alternative_link_text", "https://i.imgur.com")], matches)

	def test_extract_markdown_links_x3(self):
		matches = extract_markdown_links(
			"This is text with an [link](https://i.imgur.com)\n" +
			"This is text with an [marketing](https://marketing.com/how-to-start)\n" +
			"This is text with an [social](https://facbook.com/marketing-guru)"
		)
		self.assertListEqual([
			("link", "https://i.imgur.com"),
			("marketing", "https://marketing.com/how-to-start"),
			("social", "https://facbook.com/marketing-guru")
		], matches)


	def test_split_images(self):
		node = TextNode(
			"This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT,
		)
		new_nodes = split_nodes_image([node])
		self.assertListEqual(
			[
				TextNode("This is text with an ", TextType.TEXT),
				TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
			],
			new_nodes,
		)

	def test_split_images_x2(self):
		node = TextNode(
			"This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
			TextType.TEXT,
		)
		new_nodes = split_nodes_image([node])
		self.assertListEqual(
			[
				TextNode("This is text with an ", TextType.TEXT),
				TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
				TextNode(" and another ", TextType.TEXT),
				TextNode(
					"second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
				),
			],
			new_nodes,
		)

	def test_split_link(self):
		node = TextNode(
			"This is text with an [link](https://i.imgur.com)",
			TextType.TEXT,
		)
		new_nodes = split_nodes_link([node])
		self.assertListEqual(
			[
				TextNode("This is text with an ", TextType.TEXT),
				TextNode("link", TextType.IMAGE, "https://i.imgur.com"),
			],
			new_nodes,
		)

	def test_split_link_x2(self):
		node = TextNode(
			"This is text with an [link](https://i.imgur.com) and another [second link](https://i.imgur.com)",
			TextType.TEXT,
		)
		new_nodes = split_nodes_link([node])
		self.assertListEqual(
			[
				TextNode("This is text with an ", TextType.TEXT),
				TextNode("link", TextType.IMAGE, "https://i.imgur.com"),
				TextNode(" and another ", TextType.TEXT),
				TextNode("second link", TextType.IMAGE, "https://i.imgur.com"),
			],
			new_nodes,
		)
if __name__ == "__main__":
	unittest.main()