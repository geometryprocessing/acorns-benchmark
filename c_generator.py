#------------------------------------------------------------------------------
# autodiff: c_generator.py
#
# C code generator from autodiff nodes.
#
#------------------------------------------------------------------------------


class CGenerator(object):
	"""Writes a file with C code, hardcoded function definitions,
		uses string accumulation for returning expressions.
	"""

	def __init__(self, filename = 'c_code', variable_count = 1, derivative_count = 1, ispc = True, c_code = False, split=False, split_index=0,
		split_by  = 20):
		self.indent_level = 0
		self.filename=filename
		self.variable_count = variable_count # number of variables
		self.derivative_count = derivative_count # number of derivatives
		self.count = 0
		self.ispc = ispc
		self.c_code = c_code
		self.split = split
		print(split_index)
		if self.split:
			print("opening file : "+self.filename+'{}.c'.format(split_index))
			f = open(self.filename+'{}.c'.format(split_index),'w')
			f.close()
		else:
			f = open(self.filename+'.txt','w')
			f.close()
		self.split_by = split_by
		self.split_index = str(split_index)

	def _make_indent(self):
		return ' ' * self.indent_level

	def _make_header(self):

		if self.c_code:
			ext = '.txt'
			if self.split:
                
                
				ext = '.c'
                
				# make header
				if self.split_index=='0':
					print("Overwrite previous header files: ",self.filename)
					f = open(self.filename+'.h','w')
				else:
					f = open(self.filename+'.h','a')
                    
				f.write("void compute_"+str(self.split_index)+"(int num_points, double ders[], double grads[], double vjac_it[], double da[], double local_disp[], double mu, double lambda);\n\n")
				f.close()
                
                
                
                
				f = open(self.filename+self.split_index+ext,'w')
				f.write("#include <assert.h>\n#include <time.h>\n#include <math.h>\n#include <stdlib.h>\n#include <stdio.h>\n#include <stdint.h>\n")
				f.write("void compute_"+str(self.split_index)+"(int num_points, double ders[], double grads[], double vjac_it[], double da[], double local_disp[], double mu, double lambda){\n\n")
				f.write("int i=0;\n")
				f.write("\tfor(int p = 0; p < num_points; ++p)\n\t{\n") # iterate over 
				f.close()				
			else:
				f = open(self.filename+ext,'w')
				f.write("#include <assert.h>\n#include <time.h>\n#include <math.h>\n#include <stdlib.h>\n#include <stdio.h>\n#include <stdint.h>\n")
				f.write("void compute(int num_points, double ders[], double grads[], double vjac_it[], double da[], double local_disp[], double mu, double lambda){\n\n")
				f.write("int i=0;\n")
				f.write("\tfor(int p = 0; p < num_points; ++p)\n\t{\n") # iterate over 
				f.close()

	def _make_header_forward(self):

		ext = '.txt'
		f = open(self.filename+ext,'a')
		f.write("\n\n\ndouble forward(int num_points, double energy, double grads[], double vjac_it[], double da[], double local_disp[], double mu, double lambda){\n\n")
		f.write("int i=0;\n")

		f.write("\tfor(int p = 0; p < num_points; ++p)\n\t{\n") # iterate over 
		f.close()


	def _generate_expr(self, var, derivative_string, index, mirrored_index=None):

		if self.c_code:

			base = ''
			if type(var) is list:
				base = 'd'+ 'd'.join(var)
			elif type(var) is str:
				base = var

			ext = '.txt'		
			if self.split:
				ext = '.c'
				f = open(self.filename+self.split_index+ext,'a')
			else:			
				f = open(self.filename+ext,'a')
			f.write("\t\tders[i*"+str(self.derivative_count)+"+"+str(index)+"]"+"+= "+derivative_string+"; // {} \n".format('df/('+base+')'))
			if index != mirrored_index and mirrored_index:
				f.write("\t\tders[i*"+str(self.derivative_count)+"+"+str(mirrored_index)+"]"+"= ders[i*"+str(self.derivative_count)+"+"+str(index)+"]; // {} \n".format('df/('+base+')'))
			f.close()					
		

	
		self.count += 1	


	def _generate_expr_forward(self, output_string):
		ext = '.txt'					
		f = open(self.filename+ext,'a')
		f.write("\t\tenergy"+"= "+output_string+"; //  \n")
		f.close()



	def _generate_copy(self, var, pointer_index, index):

		# print("VAR_STRINGS: {}".format(var_strings))

		if self.c_code:

			base = ''
			if type(var) is list:
				base = 'd'+ 'd'.join(var)
			elif type(var) is str:
				base = var

			ext = '.txt'		
			f = open(self.filename+ext,'a')
		
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

			ext = '.txt'			
			f = open(self.filename+ext,'a')
			f.write("\t\tdouble %s = values[i* %d + %d ];\n" % (var, self.variable_count, index))
			f.close()

	

	# def _footer_helper(self, test_case):
	# 	ext = '.txt'			
	# 	f = open(self.filename+ext,'a')		
	# 	f.write("void "+test_case+"() {\n ")

	# 	# 	double *ders = malloc(num_points*num_vars * sizeof(double)); \n \


	# 	f.write("printf(\"I am running...\\n\"); \n \
	# // read command line arguments \n \
	# char* ptr; \n \
	# int num_points = 12; \n \
	# int num_vars = 1; \n \
	# double *ders = malloc(12 * sizeof(double)); \n")
	# # double error = 0.01;\n")
	# 	test_case = open("testcases/"+test_case+'.txt','r')
	# 	case = test_case.readlines()
	# 	for line in case:
	# 		f.write(line)		

	# 	# for single derivative	
	# 	f.write("\n\t compute(num_points, ders, grads, vjac_it, da, local_disp); \n \
	# 	for(int i = 0; i < num_points*num_vars; i++) { \n \
	# 		printf(\"value: %f\\n\", ders[i]); \n \
	#     			\n}\n}\n")		


	#  	# for hessian
	# 	# f.write("\n\t compute(num_points, ders, grads, vjac_it, da, local_disp); \n \
	# 	# for(int i = 0; i < 36; i++) { \n \
	# 	# 	printf(\"%f\\n\", ders[i]); \n \
	#  #    			}\n}\n")
	# 	f.close()

	def _make_footer_forward(self):
		ext = '.txt'
		f = open(self.filename+ext,'a')

		f.write("\t}\n return energy;}\n\n")
		f.close()


	def _write_main(self):
		ext = '.txt'

		if self.split:
			ext = '.c'
			f = open(self.filename+self.split_index+ext,'a')
		else:			
			f = open(self.filename+ext,'a')

		f.write("\n\nint main(int argc, char* argv[]){ %s")
		# f.write("test_case_0_size3();")

		f.write("}")
		f.close()			


	def _make_footer(self):

		if self.c_code:

			ext = '.txt'			
			if self.split:
				ext = '.c'
				f = open(self.filename+self.split_index+ext,'a')
			else:			
				f = open(self.filename+ext,'a')
			f.write("\t}\n}\n\n")
			f.close()


	def _write(self,derivative_string):
		self._make_header()
		self._generate_expr(derivative_string)
		self._make_footer()



