class HTMLNode:
	def __init__(self, tag = None, value = None, children = None, props = None):
		self.tag = tag
		self.value = value
		
		if children == None:
			self.children = children
		elif isinstance(children, list):
			for i in range(len(children)):
				if not isinstance(children[i], HTMLNode):
					raise ValueError(f"children[{i}]: is not an instance of a HTMLNode")
			self.children = children
		else:
			raise ValueError(f"children is set and is not an instance of a list")

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
	
	def __eq__(self, other):
		if self.tag != other.tag:
			return False
		elif self.value != other.value:
			return False
		elif self.children != other.children:
			return False
		elif self.props != other.props:
			return False
		
		return True