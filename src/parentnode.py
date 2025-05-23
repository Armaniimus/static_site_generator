from htmlnode import HTMLNode

class ParentNode(HTMLNode):
	def __init__(self, tag, children, props = None):
		super().__init__(tag, None, children, props)
	
	def to_html(self):
		if self.tag == None or self.tag == "":
			raise ValueError("tag is required")
		
		if not isinstance(self.children, list):
			raise ValueError("children are required")
		
		inner_str = ""

		for c in self.children:
			if not isinstance(c, HTMLNode):
				raise ValueError("one of the children is not a proper HTMLNode")
			inner_str += c.to_html()

		props = self.props_to_html()
		if props != "":
			props = " " + props
		return f"<{self.tag}{props}>{inner_str}</{self.tag}>"