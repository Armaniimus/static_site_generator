import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
	def test_initialize(self):
		tag = "a"
		value = "click here"
		dic = {
			"href": "https://www.google.com",
			"target": "_blank",
		}

		node = HTMLNode(tag, value, None, dic)

		self.assertEqual(node.tag, tag)
		self.assertEqual(node.value, value)
		self.assertEqual(node.children, None)
		self.assertEqual(node.props, dic)
	
	def test_init_set_none(self):
		node = HTMLNode()
		self.assertEqual(node.tag, None)
		self.assertEqual(node.value, None)
		self.assertEqual(node.children, None)
		self.assertEqual(node.props, None)

	def test_pureDictionary(self):
		tag = "a"
		value = "click here"
		dic = {
			"href": "https://www.google.com",
			"target": "_blank",
		}

		node = HTMLNode(tag, value, None, dic)
		self.assertEqual(node.props, dic)

		dic["a"] = "b"
		self.assertNotEqual(node.props, dic)

	def test_props_to_html(self):
		tag = "a"
		value = "click here"
		dic = {
			"href": "https://www.google.com",
			"target": "_blank",
		}
		node = HTMLNode(tag, value, None, dic)

		self.assertEqual(node.props_to_html(), 'href=\"https://www.google.com\" target=\"_blank\"')

	def test_props_to_html_none(self):
		node = HTMLNode()
		self.assertEqual(node.props_to_html(), "")
if __name__ == "__main__":
		unittest.main()