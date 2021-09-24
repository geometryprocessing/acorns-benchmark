import os
import general_utils

def generate_adept_file(func_num, num_params, functions, params_filename):
    with open('./tests/utils/static_code/adept_single.txt', 'r') as file:
        adept = file.read()
        adept_file = open("./tests/utils/adept_jacobian.cpp", "w+")
        num_vars = len(functions[func_num][1])
        vars = functions[func_num][1]
        function = functions[func_num][0]
        aVetors = generate_aVectors(vars)
        vector_init = generate_vector_initialization(vars)
        ders = der_set(vars)
        cpp_code = adept % (num_params, num_vars, aVetors, params_filename, vector_init, function, ders)
        adept_file.write(cpp_code)
        adept_file.close()     

def compile_adept(compiler_version=""):
    os.system(f"g++{compiler_version} ./tests/utils/adept_jacobian.cpp -o ./tests/utils/runnable_adept_jacobian -L/usr/local/lib -Wl,-rpath,/usr/local/lib -ladept -I ./tests/utils/ext/ -O3 -ffast-math")

def run_adept():
    os.system("./tests/utils/runnable_adept_jacobian ./tests/utils/adept_jacobian_output.txt")
    return general_utils.parse_output("./tests/utils/adept_jacobian_output.txt")

def generate_aVectors(vars):
    aVectors_str = ""
    for i, var in enumerate(vars):
        aVectors_str += f" {var}(num_params)"

        if i != len(vars) - 1:
            aVectors_str += ","
    aVectors_str += ";"
    return aVectors_str

def generate_vector_initialization(vars):
    init_str = ""
    for i, var in enumerate(vars):
        init_str += f"\t\t\t{var}(index) = args[index * num_vars + {i}];"
        if i != len(vars) - 1:
            init_str += "\n"
    return init_str

def der_set(vars):
    der_str = ""
    for i, var in enumerate(vars):
        der_str += f"\t\t\tders[index * num_vars + {i}] = {var}.get_gradient()[index];"
        if i != len(vars) - 1:
            der_str += "\n"
    return der_str  


