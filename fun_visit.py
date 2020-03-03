from __future__ import print_function
import sys
from collections import namedtuple
import math
from pycparser import parse_file
from pycparser import c_parser
import pycparser.c_ast
import c_generator
import argparse
import numpy as np

class Generator(pycparser.c_ast.Node):
	"""
	Return stirng accumulation of expanded equations
	"""
	def __init__(self):
		self.indent_level = 0
		self.variables = {}
		self.names_vars= []
		self.symbols = []
		self.thresholds = []
		self.names_vars_init = []

	def _make_indent(self):
		return ' ' * self.indent_level

	def visit(self, node, subscript = False):
		method = 'visit_' + node.__class__.__name__
		# print("visit node",method)
		
		if subscript:
			return getattr(self, method)(node, subscript)
		else:
			return getattr(self, method)(node)


	def visit_Constant(self, n, subscript=False):
		return n.value

	def visit_ID(self, n, subscript=False):
		if subscript:
			if n.name in self.variables.keys():
				# print(self.variables)
				return self.variables[n.name]

		return n.name

	def generic_visit(self, node):
	    #~ print('generic:', type(node))
		if node is None:
			return ''
		else:
			# print("Generic visit understanding")
			# for c_name, c in node.children():
			# 	print(c_name)
			# print(node.children())
			return "bye"

			# return ''.join(self.visit(c) for c_name, c in node.children())		

	def visit_FuncCall(self, n):
		if (n.name.name) == 'log':
			value = self.variables[self.visit(n.args.exprs[0])]

		return 'log({})'.format(value)

	def visit_BinaryOp(self, n, subscript=False):
		# print("Enter binary op",n,subscript)
		if n.op == '+':
			left = self.visit(n.left, subscript=subscript)
			right = self.visit(n.right, subscript=subscript)


			if type(left).__name__ == 'list':
				
				arr_subscripts = self.flatten(left,[])
				left = arr_subscripts[0]+'[{}]'*len(arr_subscripts[1:])
				left = left.format(*arr_subscripts[1:])
				# arr_string = arr_subscripts[0]+'[{}]'*len(arr_subscripts[1:])
				# arr_val = [self.variables[item] for item in arr_subscripts[1:]]
				# left = arr_string.format(*arr_val)

			if type(right).__name__ == 'list':
				arr_subscripts = self.flatten(right,[])
				right = arr_subscripts[0]+'[{}]'*len(arr_subscripts[1:])
				right = right.format(*arr_subscripts[1:])
				# arr_string = arr_subscripts[0]+'[{}]'*len(arr_subscripts[1:])
				# arr_val = [self.variables(item) for item in arr_subscripts[1:]]
				# right = arr_string.format(*arr_val)

			if left in self.variables:
				left = self.variables[left]
			if right in self.variables:
				right = self.variables[right]

			if left.isnumeric() and right.isnumeric():
				return str(int(left)+int(right))

			# print("in addition")
			# print(left)
			# print(right)
			# print("=======================")
			return "("+left +") + ("+right+")"	
		elif n.op == '*':
			left = self.visit(n.left, subscript = subscript)
			right = self.visit(n.right, subscript = subscript)

			# print(n)
			# print("left:",left)
			# print("right: ",right)

			if type(left).__name__ == 'list':
				arr_subscripts = self.flatten(left,[])
				left = arr_subscripts[0]+'[{}]'*len(arr_subscripts[1:])
				left = left.format(*arr_subscripts[1:])
				# arr_subscripts = self.flatten(left)
				# arr_string = arr_subscripts[0]+'[{}]'*len(arr_subscripts[1:])
				# arr_val = [self.variables[item] for item in arr_subscripts[1:]]
				# left = arr_string.format(*arr_val)

			if type(right).__name__ == 'list':
				arr_subscripts = self.flatten(right,[])
				right = arr_subscripts[0]+'[{}]'*len(arr_subscripts[1:])
				right = right.format(*arr_subscripts[1:])
				# arr_subscripts = self.flatten(right)

				# arr_string = arr_subscripts[0]+'[{}]'*len(arr_subscripts[1:])
				# arr_val = [self.variables(item) for item in arr_subscripts[1:]]
				# right = arr_string.format(*arr_val)


			if left in self.variables:
				left = self.variables[left]
			if right in self.variables:
				right = self.variables[right]

			if left.isnumeric() and right.isnumeric():
				return str(int(left)*int(right))

			return "("+left +") * ("+right+")"	
		elif n.op == '-':
			left = self.visit(n.left, subscript = subscript)
			right = self.visit(n.right, subscript = subscript)

			# print(n)
			# print("left:",left)
			# print("right: ",right)

			if type(left).__name__ == 'list':
				arr_subscripts = self.flatten(left,[])
				left = arr_subscripts[0]+'[{}]'*len(arr_subscripts[1:])
				left = left.format(*arr_subscripts[1:])
				# arr_subscripts = self.flatten(left)
				# arr_string = arr_subscripts[0]+'[{}]'*len(arr_subscripts[1:])
				# arr_val = [self.variables[item] for item in arr_subscripts[1:]]
				# left = arr_string.format(*arr_val)

			if type(right).__name__ == 'list':
				arr_subscripts = self.flatten(right,[])
				right = arr_subscripts[0]+'[{}]'*len(arr_subscripts[1:])
				right = right.format(*arr_subscripts[1:])
				# arr_subscripts = self.flatten(right)

				# arr_string = arr_subscripts[0]+'[{}]'*len(arr_subscripts[1:])
				# arr_val = [self.variables(item) for item in arr_subscripts[1:]]
				# right = arr_string.format(*arr_val)


			if left in self.variables:
				# print('substituting ',left,' with value ',self.variables[left])
				left = self.variables[left]
			if right in self.variables:
				right = self.variables[right]


			if left.isnumeric() and right.isnumeric():
				return str(int(left)-int(right))

			return "("+left +") - ("+right+")"	
		elif n.op == '/':
			left = self.visit(n.left, subscript = subscript)
			right = self.visit(n.right, subscript = subscript)


			if type(left).__name__ == 'list':
				arr_subscripts = self.flatten(left,[])
				left = arr_subscripts[0]+'[{}]'*len(arr_subscripts[1:])
				left = left.format(*arr_subscripts[1:])
				# arr_subscripts = self.flatten(left)
				# arr_string = arr_subscripts[0]+'[{}]'*len(arr_subscripts[1:])
				# arr_val = [self.variables[item] for item in arr_subscripts[1:]]
				# left = arr_string.format(*arr_val)

			if type(right).__name__ == 'list':
				arr_subscripts = self.flatten(right,[])
				right = arr_subscripts[0]+'[{}]'*len(arr_subscripts[1:])
				right = right.format(*arr_subscripts[1:])
				# arr_subscripts = self.flatten(right)

				# arr_string = arr_subscripts[0]+'[{}]'*len(arr_subscripts[1:])
				# arr_val = [self.variables(item) for item in arr_subscripts[1:]]
				# right = arr_string.format(*arr_val)

			if left in self.variables:
				left = self.variables[left]
			if right in self.variables:
				right = self.variables[right]


			if left.isnumeric() and right.isnumeric():
				return str(int(left)/int(right))

			return "("+left +") / ("+right+")"	

	def visit_For(self, n):
		# print("For loop detected")
		# variables initialized
		names_vars_init = self.visit(n.init)

		# for loop info extracted
		symbol = n.cond.op
		threshold = self.visit(n.cond.right)

		# if threshold is a variable, give it the value
		try:
			if str(threshold)!=str(int(threshold)):
				threshold = self.variables[threshold]
		except:
			threshold = self.variables[threshold]
		

		var_name = self.visit(n.cond.left)

		# print(var_name,  symbol, threshold)

		self.symbols.append(symbol)
		self.thresholds.append(int(threshold))
		self.names_vars.append(var_name)
		self.names_vars_init.append(names_vars_init)

		# Assuming next is one increment
		# print(n.next)
		# print("Statement of loop")
		# print(n.stmt.block_items[0].__class__.__name__)
		# print(n.stmt.__class__.__name__)
		if n.stmt.__class__.__name__ == 'Compound' and n.stmt.block_items[0].__class__.__name__ == 'For':
			# print("Nested for loop detected")
			# n.stmt.show()
			loop_stmt = self.visit(n.stmt)
		else:

			np_aranges = [np.array(np.arange(0,self.thresholds[i])) for i,s in enumerate(self.names_vars)]
			# print(np_aranges)
			list_counters = np.array(np.meshgrid(*np_aranges)).T.reshape(-1,len(self.names_vars))
			# print(list_counters)

			for counter in list_counters:
				for i,item in enumerate(counter):
					self.variables[self.names_vars[i]] = str(item)
				vars_, value = self.visit(n.stmt)


				var_string = vars_[0]+'[{}]'*len(vars_[1:])
				# print("====================================")
				# print("double "+var_string.format(*vars_[1:])+' = '+ str(value)+";")
				f = open(op_filename+".c","a")
				f.write("double "+var_string.format(*vars_[1:])+' = '+ str(value)+";\n")
				f.close()
				# print("====================================")




			# print("Deleting variables: ",self.names_vars)
			for v in self.names_vars:
				del self.variables[v]
			self.names_vars=[]
			self.names_vars_init=[]
			self.thresholds = []
			self.symbols = []

			return 
		return

	def visit_ArrayRef(self, n):

		return [self.visit(n.name), self.visit(n.subscript, subscript = True)]

	def visit_Compound(self, n):
		return self.visit(n.block_items[0])
		# for block in n.block_items:
		# 	results = self.visit(block)
		# 	print("Are you here")


	def flatten(self, x, flattened):
		if type(x).__name__!='list':
			return [x]
		elif len(x)==1:
			return x[0]
		for sublist in x:
			if type(sublist).__name__ == 'str':
				flattened.append(sublist)
			elif type(sublist).__name__ == 'list':
				self.flatten(sublist, flattened)

		return flattened

	def visit_Assignment(self, n, subscript=False):
		# print("@ Assignment")
		name = self.visit(n.lvalue, subscript=subscript)
		value = self.visit(n.rvalue, subscript=subscript)
		value = self.eval_arrayref(value)
		# print("Returning stuff", self.flatten(name,[]), value)
		return self.flatten(name,[]), value

	def eval_arrayref(self, l):
		if type(l).__name__=='list':
			l = self.flatten(l,[])
			res = l[0]+'[{}]'*len(l[1:])
			return res.format(*l[1:])
		else:
			return l
	

	def visit_Decl(self, n, no_type=False):
		# no_type is used when a Decl is part of a DeclList, where the type is
		# explicitly only for the first declaration in a list.
		#
		# print(n)
		# print(n.init.__class__.__name__)
		if n.init.__class__.__name__=='BinaryOp':
			self.variables[n.name] = self.visit(n.init)
		elif n.init.__class__.__name__ == 'FuncCall':
			self.variables[n.name] = self.visit(n.init)
		else:
			self.variables[n.name] = n.init.value



		# print("New variable: ",n.name, " = ", self.variables[n.name])
		return n.name



	def visit_DeclList(self, n):
		names = []
		for decl in n.decls:
			names.append(self.visit(decl))
		return names
		# s = self.visit(n.decls[0])
		# print("in decl list")
		# print(s)
		# if len(n.decls) > 1:
		# 	s += ', ' + ', '.join(self.visit_Decl(decl, no_type=True)
		# 		for decl in n.decls[1:])
		# return s
		


        # s = 'for ('
        # if n.init: s += self.visit(n.init)
        # s += ';'
        # if n.cond: s += ' ' + self.visit(n.cond)
        # s += ';'
        # if n.next: s += ' ' + self.visit(n.next)
        # s += ')\n'
        # s += self._generate_stmt(n.stmt, add_indent=True)
        # return s



def match_item(ast):
	gen = Generator()
	if ast.block_items:
		for block in ast.block_items:
			# print('In match item')
			# print(type(block))
			# print(block)
			res = gen.visit(block)
			if type(res).__name__=='tuple':
				# print(res)
				# came from assignment or array ref. assumed assignment
				f = open(op_filename+".c","a")
				# print("double "+res[0][0]+' = '+ res[1]+";\n")
				f.write("double "+res[0][0]+' = '+ res[1]+";\n")
				f.close()


def make_graph(ast):
    fun = None

    for funs in range(len(ast.ext)):
        if 'decl' not in  dir(ast.ext[funs]):
            continue

    fun_body = ast.ext[funs].body
    match_item(fun_body)

    f = open(op_filename+".c",'a')
    f.write('\n}')
    f.close()





if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('filename', type = str, help='file name')
    # parser.add_argument('expr', type = str, help='file name')
    # parser.add_argument('-v', '--vars',
    #                   type=str, action='store',
    #                   dest='variables',
    #                   help='Variables to differentiate wrt to')
    # parser.add_argument('-func', type = str, dest = 'func', help='function name')
    parser.add_argument('op_filename', type = str, default ='output_fun', help='op file name')    



    parser = parser.parse_args()




    filename = parser.filename
    op_filename = parser.op_filename

    f = open(op_filename+".c",'w')
    f.write('int function_0(){\n')
    f.close()

    ast = parse_file(filename, use_cpp=True,
            cpp_path='gcc',
            cpp_args=['-E', r'-Iutils/fake_libc_include'])
    # ast.show()
    make_graph(ast)
    # ast.show()
    ext_index = 0

