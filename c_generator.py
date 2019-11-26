#------------------------------------------------------------------------------
# autodiff: c_generator.py
#
# C code generator from autodiff nodes.
#
#------------------------------------------------------------------------------
import math

class CGenerator(object):
	"""Writes a file with C code, hardcoded function definitions,
		uses string accumulation for returning expressions.
	"""

	def __init__(self, filename = 'c_code', variable_count = 1, derivative_count = 1, ispc = True, c_code = False, parallel = False):
		self.indent_level = 0
		self.filename=filename
		self.variable_count = variable_count # number of variables
		self.derivative_count = derivative_count # number of derivatives
		self.count = 0
		self.ispc = ispc
		self.c_code = c_code
		self.parallel = parallel
		f = open(self.filename+'.c','w')
		f.close()

	def _make_indent(self):
		return ' ' * self.indent_level

	def _make_header(self):

		if self.c_code:
			ext = '.c'

			f = open(self.filename+ext,'w')
			f.write("void compute(double values[], int num_points, double ders[]){\n\n")
			
			f.write("\tfor(int i = 0; i < num_points; ++i)\n\t{\n") # iterate over 
	
			f.close()


	def _generate_expr(self, var, derivative_string, index):

		# print("VAR_STRINGS: {}".format(var_strings))

		if self.c_code:

			base = ''
			if type(var) is list:
				base = 'd'+ 'd'.join(var)
			elif type(var) is str:
				base = var

			ext = '.c'		
			f = open(self.filename+ext,'a')
			if self.parallel:
				# for var_string in var_strings:
				# 	f.write("\t\t{};\n".format(var_string))
				# if index!=0:
				if index==0: 			
					f.write("\t#pragma omp parallel sections num_threads(4)\n")	
					f.write("\t{\n")	

				f.write("\t\t#pragma omp section\n")
				f.write("\t\t{\n")




			f.write("\t\tders[i*"+str(self.derivative_count)+"+"+str(index)+"]"+"= "+derivative_string+"; // {} \n".format('df/('+base+')'))
			if self.parallel:
				# if index!=0:			
				f.write("\t\t}\n")
			f.close()					
			
		self.count += 1	

	def _generate_copy(self, var, pointer_index, index):

		# print("VAR_STRINGS: {}".format(var_strings))

		if self.c_code:

			base = ''
			if type(var) is list:
				base = 'd'+ 'd'.join(var)
			elif type(var) is str:
				base = var

			ext = '.c'		
			f = open(self.filename+ext,'a')
			if self.parallel and pointer_index==1:
				f.write("\t}\n")		
			# if self.parallel:			

			# 	f.write("\t\t#pragma omp section\n")
			# 	f.write("\t\t{\n")

			f.write("\t\tders[i*"+str(self.derivative_count)+"+"+str(index)+"]"+"= ders[i*"+str(self.derivative_count)+"+"+str(pointer_index)+"]; // {} \n".format('df/('+base+')'))
			# if self.parallel:
			# 	f.write("\t\t}\n")
			f.close()					
		
		self.count += 1			

	def _declare_vars(self, var, index):
		if self.c_code:

			ext = '.c'			
			f = open(self.filename+ext,'a')
			f.write("\t\tdouble %s = values[i* %d + %d ];\n" % (var, self.variable_count, index))
			f.close()
			

	def _make_footer(self):
		if self.c_code:

			ext = '.c'			
			f = open(self.filename+ext,'a')
			f.write("\t}\n\t}\n\n")
			# if self.parallel:
			# 	f.write("\t}\n")
			f.close()	


	def _write(self,derivative_string):
		self._make_header()
		self._generate_expr(derivative_string)
		self._make_footer()


