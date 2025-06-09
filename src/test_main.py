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

	# def test_get_source_files(self):
	# 	i = get_source_files("./content/")
	# 	# print(i)

	def test_get_destination_file(self):
		expected = "./public/contact.html"
		
		actual  = get_destination_file("./content/contact", "./content", "./public/")

		self.assertEqual(actual, expected)

	def test_get_destination_file_bulk(self):
		data = (
			(("./content/contact/index.md", "./content", "./public/"), "./public/contact.html"),
			(("./content/blog/glorfindel/index.md", "./content", "./public/"), "./public/blog/glorfindel.html"),
			(("./content/index.md", "./content", "./public/"), "./public/index.html"),
		)
		
		for d in data:
			inputs = d[0]
			expected = d[1]

			actual  = get_destination_file(inputs[0], inputs[1], inputs[2])
			
			message = f"\nFailed: \n\tinput={inputs} \n\tactual={actual} \n\texpected={expected}"
			self.assertEqual(actual, expected, message)

if __name__ == "__main__":
	unittest.main()