import os
import shutil
from blockconverter import markdown_to_html_node

def extract_title(markdown):
	lines = markdown.split("\n")

	for l in lines:
		if (l.startswith("# ")):
			return l.lstrip("# ")
		
	raise Exception("no title added in the markdown")

def generate_page(from_path, template_path, dest_path, basepath):
	print(f"\nGenerating page from {from_path} to {dest_path} using {template_path}")

	f = open(from_path, "r")
	markdown = f.read()
	f.close()

	f = open(template_path, "r")
	template = f.read()
	f.close()

	content =  markdown_to_html_node(markdown).to_html()
	title = extract_title(markdown)

	result = template.replace("{{ Content }}", content).replace("{{ Title }}", title)
	result.replace('href="/', f'href="{basepath}')
	result.replace('src="/', f'src="{basepath}')
	
	f = open(dest_path, "w")
	f.write(result)
	f.close()

def get_source_files(source):
	items = os.listdir(source)
	result = []
	for i in items:
		path = f"{source}{i}"
		if os.path.isfile(path):
			result.append(path)
		else:
			result = result + get_source_files(f"{path}/")
	
	return result

def get_destination_file(source, source_folder, dest_folder):
	split_source = source.split("/")
	split_source_folder = source_folder.split("/")

	remove_length = 0
	for i in range(len(split_source_folder)):
		if (split_source[i] == split_source_folder[i]):
			remove_length += 1
		else:
			break
	
	last_index = split_source[-1:]
	if last_index == ["index.md"]:
		url = "/".join(split_source[remove_length:-1])
	else:
		url = "/".join(split_source[remove_length:])

	if url == "" and source != "":
		return f"{dest_folder}index.html"
	else:
		return f"{dest_folder}{url}/index.html"
	
def get_content_generation_info(source, destination):
	source_urls = get_source_files(source)

	out = []

	for su in source_urls:
		destination_url = get_destination_file(su, source, destination)
		out.append({"source": su, "destination": destination_url})

	return out

def generate_content_folder(source, template_path, destination, basepath ):
	urls = get_content_generation_info(source, destination)

	for u in urls:
		create_parent_folders(u["destination"])
		generate_page(u["source"], template_path, u["destination"], basepath)

def create_parent_folders(path):
	path_list = path.split("/")
	path = ""
	for p in path_list:	
		path += f"{p}/"
		if not os.path.isfile(path):
			if ".html" in path:
				continue
			elif not os.path.exists(path):
				os.mkdir(path)
				

		

		