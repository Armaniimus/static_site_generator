import unittest
from main_utils import extract_title, get_source_files, get_destination_file
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

	def test_get_source_files(self):
		i = get_source_files("./content/")
		# print(i)

	def test_get_destination_file(self):
		i = get_destination_file("./content/index.md", "./content/", "./public/")
		# print(i)

		
if __name__ == "__main__":
	unittest.main()