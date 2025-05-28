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

class TestSplitNodes(unittest.TestCase):
	def test_get_split_node_returns_list(self):
		node = TextNode("This is text with a `code block` word", TextType.TEXT)
		split_func = get_split_node("`", node.text_type, TextType.CODE)
		actual_nodes = split_func(node)

		self.assertEqual(isinstance(actual_nodes, list), True)

	def test_split_code(self):
		node = TextNode("This is text with a `code block` word", TextType.TEXT)
		expected_nodes = [
			TextNode("This is text with a ", TextType.TEXT),
			TextNode("code block", TextType.CODE),
			TextNode(" word", TextType.TEXT),
		]
		
		actual_nodes = split_nodes_code([node])

		self.assertEqual(actual_nodes, expected_nodes)

	def test_split_code_x2(self):
		node = TextNode("This is text with a `code block` word and `another code block` word", TextType.TEXT)
		expected_nodes = [
			TextNode("This is text with a ", TextType.TEXT),
			TextNode("code block", TextType.CODE),
			TextNode(" word and ", TextType.TEXT),
			TextNode("another code block", TextType.CODE),
			TextNode(" word", TextType.TEXT)
		]
		
		actual_nodes = split_nodes_code([node])

		self.assertEqual(actual_nodes, expected_nodes)

	def test_split_nodes_delimiter_no_end(self):
		node = TextNode("This is text with a `code block`", TextType.TEXT)
		expected_nodes = [
			TextNode("This is text with a ", TextType.TEXT),
			TextNode("code block", TextType.CODE),
		]
		
		actual_nodes = split_nodes_code([node])

		self.assertEqual(actual_nodes, expected_nodes)

	def test_split_nodes_delimiter_no_start(self):
		node = TextNode("`code block` word", TextType.TEXT)
		expected_nodes = [
			TextNode("code block", TextType.CODE),
			TextNode(" word", TextType.TEXT),
		]
		
		actual_nodes = split_nodes_code([node])

		self.assertEqual(actual_nodes, expected_nodes)

	def test_split_bold(self):
		node = TextNode("This is text with a **bold word** word", TextType.TEXT)
		expected_nodes = [
			TextNode("This is text with a ", TextType.TEXT),
			TextNode("bold word", TextType.BOLD),
			TextNode(" word", TextType.TEXT),
		]
		
		actual_nodes = split_nodes_bold([node])

		self.assertEqual(actual_nodes, expected_nodes)

	def test_split_italic(self):
		node = TextNode("This is text with a _italic word_ word", TextType.TEXT)
		expected_nodes = [
			TextNode("This is text with a ", TextType.TEXT),
			TextNode("italic word", TextType.ITALIC),
			TextNode(" word", TextType.TEXT),
		]
		
		actual_nodes = split_nodes_italic([node])

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
		actual_nodes = split_nodes_link([node])
		self.assertListEqual(
			[
				TextNode("This is text with an ", TextType.TEXT),
				TextNode("link", TextType.LINK, "https://i.imgur.com"),
			],
			actual_nodes,
		)

	def test_split_link_x2(self):
		node = TextNode(
			"This is text with an [link](https://i.imgur.com) and another [second link](https://i.imgur.com)",
			TextType.TEXT,
		)
		
		actual_nodes = split_nodes_link([node])
		self.assertListEqual(
			[
				TextNode("This is text with an ", TextType.TEXT),
				TextNode("link", TextType.LINK, "https://i.imgur.com"),
				TextNode(" and another ", TextType.TEXT),
				TextNode("second link", TextType.LINK, "https://i.imgur.com"),
			],
			actual_nodes,
		)

class TestTextToTextnodes(unittest.TestCase):
	def test_combine_nodes_img_link(self):
		text = text = "This is a **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
		expected_nodes = [
			TextNode("This is a **text** with an _italic_ word and a `code block` and an ", TextType.TEXT),
			TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
			TextNode(" and a ", TextType.TEXT),
			TextNode("link", TextType.LINK, "https://boot.dev"),
		]
		
		stage0_nodes = [TextNode(text, TextType.TEXT)]
		stage1_nodes = split_nodes_image(stage0_nodes)
		actual_nodes = split_nodes_link(stage1_nodes)

		self.assertListEqual(expected_nodes, actual_nodes)

	def test_combine_nodes(self):
		text = text = "This is a **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
		expected_nodes = [
			TextNode("This is a ", TextType.TEXT),
			TextNode("text", TextType.BOLD),
			TextNode(" with an ", TextType.TEXT),
			TextNode("italic", TextType.ITALIC),
			TextNode(" word and a ", TextType.TEXT),
			TextNode("code block", TextType.CODE),
			TextNode(" and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)", TextType.TEXT)
		]
		
		stage0_nodes = [TextNode(text, TextType.TEXT)]

		stage3_nodes = split_nodes_bold(stage0_nodes)
		stage4_nodes = split_nodes_code(stage3_nodes)
		actual_nodes = split_nodes_italic(stage4_nodes)

		self.assertListEqual(expected_nodes, actual_nodes)

	def test_text_to_textnodes_complete(self):
		text = "This is a **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
		expected_nodes = [
			TextNode("This is a ", TextType.TEXT),
			TextNode("text", TextType.BOLD),
			TextNode(" with an ", TextType.TEXT),
			TextNode("italic", TextType.ITALIC),
			TextNode(" word and a ", TextType.TEXT),
			TextNode("code block", TextType.CODE),
			TextNode(" and an ", TextType.TEXT),
			TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
			TextNode(" and a ", TextType.TEXT),
			TextNode("link", TextType.LINK, "https://boot.dev"),
		]

		actual_nodes = text_to_textnodes(text)

		self.assertListEqual(expected_nodes, actual_nodes)
if __name__ == "__main__":
	unittest.main()