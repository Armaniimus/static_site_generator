# import os
from blockconverter import markdown_to_html_node

def extract_title(markdown):
	lines = markdown.split("\n")

	for l in lines:
		if (l.startswith("# ")):
			return l.lstrip("# ")
		
	raise Exception("no title added in the markdown")

def generate_page(from_path, template_path, dest_path):
	print(f"Generating page from {from_path} to {dest_path} using {template_path}")

	f = open(from_path, "r")
	markdown = f.read()
	f.close()

	f = open(template_path, "r")
	template = f.read()
	f.close()

	content =  markdown_to_html_node(markdown).to_html()
	title = extract_title(markdown)

	result = template.replace("{{ Content }}", content).replace("{{ Title }}", title)
	
	f = open(dest_path, "w")
	f.write(result)
	f.close()

	