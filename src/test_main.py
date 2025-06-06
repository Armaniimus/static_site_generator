import unittest
from main_utils import extract_title, generate_page
class TestMain(unittest.TestCase):
	def test_extract_title(self):
		input = "# Hello"
		expected = "Hello"

		actual = extract_title(input)

		message = f"\nFailed: \n\tinput={input} \n\tactual={actual} \n\texpected={expected}"
		self.assertEqual(actual, expected, message)

	def test_extract_title_exception(self):
		with self.assertRaises(Exception):
			extract_title("blank")

	def test_generate_page(self):
		generate_page("./content/index.md", "./template.html", "./public/index.html")

		
if __name__ == "__main__":
	unittest.main()