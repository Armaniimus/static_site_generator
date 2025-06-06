import os
import shutil
from main_utils import extract_title

def main():
	__clear_public()
	__add_static_files()

	# markdown = ""
	# title = __extract_title(markdown)	

def __add_static_files():
	path = "./public"
	if not os.path.exists(path):
		os.mkdir("./public")
		print("log=> created ./public directory")
	
	if not os.path.exists("./static"):
		os.mkdir("./static")
		print("log=> created ./static directory")

	print("log=> start __copy_dir")
	__copy_dir("./static", "./public")
		
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


def __clear_public():
	path = "./public"
	if os.path.exists(path):
		print("log=> ./public exists\nlog=> removing ./public")
		
		message = f"log=> shutil.rmtree({path}): succeeded\nlog=> ./public removed"
		def onerror(): nonlocal message; message = f"shutil.rmtree({path}): failed"
		
		shutil.rmtree(path, onerror=onerror)
		print(message)
			
	else:
		print("log=> public doesn't exist on path:" + path)
		print(f"log=> localdirs: {os.listdir('./')}")
main()