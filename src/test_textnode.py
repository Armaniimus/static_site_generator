import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
	def test_eq(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a text node", TextType.BOLD)
		
		self.assertEqual(node, node2)

	def test_unequal(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is", TextType.BOLD)
		node3 = TextNode("This is a text node", TextType.NORMAL)

		self.assertNotEqual(node, node2)
		self.assertNotEqual(node, node3)

	def test_is_url_none(self):
		node = TextNode("This is a text node", TextType.BOLD)

		self.assertEqual(node.url, None)
	
	def test_is_url_set(self):
		node = TextNode("This is a text node", TextType.IMAGE, "./a.jpg")

		self.assertEqual(node.url, "./a.jpg")


class TestTextNodeToHtml(unittest.TestCase):
	def test_text(self):
		node = TextNode("This is a text node", TextType.NORMAL)
		html_node = node.to_html_node()
		self.assertEqual(html_node.tag, None)
		self.assertEqual(html_node.value, "This is a text node")
	
	def test_bold(self):
		node = TextNode("This is a text node", TextType.BOLD)
		html_node = node.to_html_node()
		self.assertEqual(html_node.tag, "b")
		self.assertEqual(html_node.value, "This is a text node")
	
	def test_italic(self):
		node = TextNode("This is a text node", TextType.ITALIC)
		html_node = node.to_html_node()
		self.assertEqual(html_node.tag, "i")
		self.assertEqual(html_node.value, "This is a text node")

	def test_code(self):
		node = TextNode("This is a text node", TextType.CODE)
		html_node = node.to_html_node()
		self.assertEqual(html_node.tag, "code")
		self.assertEqual(html_node.value, "This is a text node")
	
	def test_link(self):
		node = TextNode("This is a text node", TextType.LINK, "http://abc.com")
		html_node = node.to_html_node()
		self.assertEqual(html_node.tag, "a")
		self.assertEqual(html_node.value, "This is a text node")
		self.assertEqual(html_node.props, {"href": "http://abc.com"})

	def test_image(self):
		node = TextNode("This is a text node", TextType.IMAGE, "http://abc.jpg")
		html_node = node.to_html_node()
		self.assertEqual(html_node.tag, "img")
		self.assertEqual(html_node.value, None)
		self.assertEqual(html_node.props, {"alt": "This is a text node", "src": "http://abc.jpg"})

if __name__ == "__main__":
		unittest.main()