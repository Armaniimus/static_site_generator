class HTMLNode:
	def __init__(self, tag = None, value = None, children = None, props = None):
		self.tag = tag
		self.value = value
		self.children = children

		if props != None:
			self.props = dict(props)
		else:
			self.props = None
		
	def to_html(self):
		raise Exception ("NotImplementedError")
	
	def props_to_html(self):
		if self.props == None:
			return ""

		prop_str = ""
		for key in self.props:
			if prop_str != "":
				prop_str += " "

			value = self.props[key]
			prop_str += f'{key}=\"{value}\"'
		return prop_str
	
	def __repr__(self):
		return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"