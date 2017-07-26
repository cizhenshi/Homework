class Attribute(object):
	def __init__(self):
		self.str = ""
		self.type = ""
		self.name= ""
		self.lineno = -1
		self.extend = []
		self.value = None
		self.parameter_list = []
		self.sublist = []
		self.dimension = 0
		self.var_list = []

class SymbolTable(object):
	"""docstring for Symbol_table"""
	def __init__(self):
		self.table = []
		#name type F_Type F_const declare_line extend
		self.domain_stack = []
		self.domain_stack.append(0)
		self.Top = 0      #current position in symbol table
	def rollback(self):
		self.table = []
		#name type F_Type F_const declare_line extend
		self.domain_stack = []
		self.domain_stack.append(0)
		self.Top = 0      #current position in symbol table
	#根据ID.name查找符号表
	def find(self, str, mode=0):
		if mode == 0:
			for i in range(0, len(self.table)):
				if self.table[i]["name"] == str:
					return True
			return False
		else:
			for i in range(self.domain_stack[-1], len(self.table)):
				if self.table[i]["name"] == str:
					return True
			return False

	def find_item(self, str):
		for i in range(0, len(self.table)):
			if self.table[i]["name"] == str:
				return i
		return None
	#向符号表插入条目插入
	def insert(self,item):
		self.Top += 1
		self.table.append(item)

	def insert_record(self, subitem):
		self.table[self.Top-1]["extend"].append(subitem)

	#定位
	def locate(self):
		self.domain_stack.append(self.Top)

	#重定位
	def relocate(self):
		i = 0
		number = self.Top - self.domain_stack[1]
		for i in range(0, number - 1):
			self.table.pop()
			self.Top -= 1
		self.domain_stack.pop()


	def get(self, name):
		length = len(self.table)
		for i in range(1, length+1):
			if self.table[length-i]["name"] == name:
				return self.table[length-i]
		return None

	def get_type(self, name):
		index = 0
		for i in range(0, len(self.table)):
			if self.table[i]["name"] == name:
				index = i
		return self.table[index]["type"]

	def get_real_type(self, name):
		index = 0
		for i in range(0, len(self.table)):
			if self.table[i]["name"] == name:
				index = i
		type = self.table[index]["type"]
		if type == "":
			return None
		elif type in ["record", "int", "char", "float", "boolean", "function", "procedure"] or type[0:5] == "array":
			return type
		else:
			return self.get_real_type(type)

	def get_extend(self, name):
		index = 0
		find = False
		for i in range(0, len(self.table)):
			if self.table[i]["name"] == name:
				index = i
				find = True
				break
		if find == False:
			return None
		type = self.table[index]["type"]
		if type == "":
			return None
		elif type in ["record", "int", "char", "float", "boolean", "function", "procedure"] or type[0:5] == "array":
			return self.table[index]["extend"]
		else:
			return self.get_extend(type)

	def get_dimension(self, name):
		index = 0
		for i in range(0, len(self.table)):
			if self.table[i]["name"] == name:
				index = i
		while self.table[index]["F_type"] != False:
			index=self.get(self.table[index]["name"])
		return self.table[index]["extend"]

#遍历列表
def find_type(list,name):
	for i in range(0,len(list)):
		if list[i]["name"] == name :
			return list[i]
	return False



