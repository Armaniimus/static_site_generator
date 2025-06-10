import sys
import os
import shutil
# from main_utils import generate_page
from main_utils import generate_content_folder

def main():
	basepath = sys.argv[0]
	if basepath == None:
		basepath = "/"

	__clear_docs()
	__add_static_files()
	
	generate_content_folder("./content/", "./template.html", "./docs/", basepath)

def __add_static_files():
	path = "./docs"
	if not os.path.exists(path):
		os.mkdir("./docs")
		print("log=> created ./docs directory")
	
	if not os.path.exists("./static"):
		os.mkdir("./static")
		print("log=> created ./static directory")

	print("log=> start __copy_dir")
	__copy_dir("./static", "./docs")
		
def __copy_dir(source, destination):
	items = os.listdir(source)

	for i in items:
		src = f"{source}/{i}"
		dest = f"{destination}/{i}"
		if os.path.isfile(src):
			shutil.copy(src, dest)
			print(f"\t\tcopied file: {src}")
		else:
			os.mkdir(dest)
			print(f"\tcopied folder: {src}")
			__copy_dir(src, dest)


def __clear_docs():
	path = "./docs"
	if os.path.exists(path):
		print("log=> ./docs exists\nlog=> removing ./docs")
		
		message = f"log=> shutil.rmtree({path}): succeeded\nlog=> ./docs removed"
		def onerror(): nonlocal message; message = f"shutil.rmtree({path}): failed"
		
		shutil.rmtree(path, onerror=onerror)
		print(message)
			
	else:
		print("log=> docs doesn't exist on path:" + path)
		print(f"log=> localdirs: {os.listdir('./')}")
main()