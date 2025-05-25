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
		node3 = TextNode("This is a text node", TextType.TEXT)

		self.assertNotEqual(node, node2)
		self.assertNotEqual(node, node3)

	def test_is_url_none(self):
		node = TextNode("This is a text node", TextType.BOLD)

		self.assertEqual(node.url, None)
	
	def test_is_url_set(self):
		node = TextNode("This is a text node", TextType.IMAGE, "./a.jpg")

		self.assertEqual(node.url, "./a.jpg")
if __name__ == "__main__":
		unittest.main()