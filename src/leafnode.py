from htmlnode import HTMLNode

class LeafNode(HTMLNode):
	def __init__(self, tag, value, props = None):
		super().__init__(tag, value, None, props)
		
	def to_html(self):		
		if self.value == None:
			value = ""
		else:
			value = self.value
	
		if self.tag == None:
			return value
		
		props = self.props_to_html()
		if props != "":
			props = " " + props

		return f"<{self.tag}{props}>{value}</{self.tag}>"