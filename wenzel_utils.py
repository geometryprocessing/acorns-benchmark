import os
import general_utils

def generate_wenzel_file(func_num, num_params, functions, params_filename, degree):
    if degree == 'single':
        with open('static_code/wenzel_single.txt', 'r') as file:
            wenzel = file.read()
            wenzel_file = open("wenzel_single.cpp", "w+")
            num_vars = len(functions[func_num][1])
            derivatives = generate_wenzel_ders(func_num, num_vars, functions, degree)
            cpp_code = wenzel % (num_vars, num_params, num_vars, params_filename, num_vars, derivatives)
            wenzel_file.write(cpp_code)
            wenzel_file.close()
    else:
        with open('static_code/wenzel_hessian.txt', 'r') as file:
            wenzel = file.read()  
            wenzel_file = open("wenzel_hessian.cpp", "w+")
            num_vars = len(functions[func_num][1])
            derivatives = generate_wenzel_ders(func_num, num_vars, functions, degree)
            cpp_code = wenzel % (num_vars, num_vars, num_vars, num_params, num_vars, params_filename, num_vars, derivatives)
            wenzel_file.write(cpp_code)
            wenzel_file.close()

def compile_wenzel(degree):
    if degree == 'single':
        os.system("g++ -DNDEBUG -std=c++11 -I utils/ext/ wenzel_single.cpp -o wenzel_single -ffast-math -O3")
    else:
        os.system("g++ -DNDEBUG -std=c++11 -I utils/ext/ wenzel_hessian.cpp -o wenzel_hessian -ffast-math -O3")

def run_wenzel(degree):
    if degree == 'single':
        os.system("./wenzel_single wenzel_output_single.txt")
        return general_utils.parse_output("wenzel_output_single.txt")
    else:
        os.system("./wenzel_hessian wenzel_output_hessian.txt")
        return general_utils.parse_output("wenzel_output_hessian.txt")

def generate_wenzel_ders(func_num, num_vars, functions, degree):
    ders_string = "\t\tDScalar "
    for i, var in enumerate(functions[func_num][1]):
        ders_string += "{}({}, args[index * {} + {}])".format(var, i, num_vars, i)
        if i == num_vars - 1:
            ders_string += ";\n"
        else:
            ders_string += ", "
    func_string = "\t\tDScalar Fx = {};\n".format(functions[func_num][0])
    grad_string = ""
    if degree == "single":
        for i in range(num_vars):
            grad_string += "\t\tders[index * {} + {}] = Fx.getGradient()({});".format(num_vars, i, i) 
            if i != num_vars - 1:
                grad_string += "\n"
    else:
        num_ders = (int) ((num_vars * (num_vars + 1)) / 2)
        for i in range(num_ders):
            grad_string += "\t\tders[index * {} + {}] = Fx.getHessian()({});".format(num_ders, i, i) 
            if i != num_vars - 1:
                grad_string += "\n"
    return ders_string + func_string + grad_string