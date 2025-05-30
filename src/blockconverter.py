def markdown_to_blocks(markdown):
	blocks = markdown.split("\n\n")

	for key in range(len(blocks)):
		blocks[key] = blocks[key].strip().strip("\n").replace(' \n','\n')

	func = lambda block: block != ""
	filtered_blocks = list( filter(func, blocks) )
	
	return filtered_blocks