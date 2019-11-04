import sys
import math
import matplotlib.pyplot as plt
import torch
from timeit import default_timer as timer
import os
from subprocess import PIPE, run
import forward_diff
import numpy as np
import shutil

import us_utils
import wenzel_utils

def generate_params(num_params, function_num):
    print("Generating params for function_num", function_num) #, " which is: ", functions[function_num][0])
    num_variables = len(functions[function_num][1])
    function_params = np.zeros(shape=(num_variables, num_params))
    for i, var in enumerate(functions[function_num][1]):
        variable_params = np.random.rand(num_params) * 10
        # np.save("utils/numpy_params/function_{}_param_{}.npy".format(function_num, var), variable_params)
        function_params[i] = variable_params
    reshaped = np.reshape(function_params, num_params*num_variables, order='F')
    param_string = "\n".join(str(x) for x in reshaped)
    param_f = open("params.txt", "w+")
    param_f.write(param_string)
    param_f.close()
    return reshaped

def print_param_to_file(params):
    param_string = "\n".join(str(x) for x in params)
    param_f = open(PARAMS_FILENAME, "w+")
    param_f.write(param_string)
    param_f.close()

def cleanup():
    if os.path.exists(INPUT_FILENAME):
        os.remove(INPUT_FILENAME)
    if os.path.exists(DERIVATIVES_FILENAME):
        os.remove(DERIVATIVES_FILENAME)
    if os.path.exists(UTILS_FILENAME):
        os.remove(UTILS_FILENAME)
    if os.path.exists(RUNNABLE_FILENAME):
        os.remove(RUNNABLE_FILENAME)
    if os.path.exists(OUTPUT_FILENAME):
        os.remove(OUTPUT_FILENAME)
    if os.path.exists(NUMPY_PARAMS_FILENAME):
        os.remove(NUMPY_PARAMS_FILENAME)
    if os.path.exists(PARAMS_FILENAME):
        os.remove(PARAMS_FILENAME)
    if os.path.exists(PYTORCH_FILENAME):
        os.remove(PYTORCH_FILENAME)
    if os.path.exists(PYTORCH_OUTPUT):
        os.remove(PYTORCH_OUTPUT)

    if os.path.exists("utils/numpy_params"):
        shutil.rmtree("utils/numpy_params")
        os.mkdir("utils/numpy_params")
    if os.path.exists("utils"):
        folder = 'utils'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
    if os.path.exists("results"):
        folder = 'results'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)

def generate_graph(avg_us_single, avg_us_hessian, avg_wenzel_single, avg_wenzel_hessian, denom, func_num, function):
    plt.figure(1)
    plt.subplot(211)
    plt.plot(denom, avg_us_single,
             denom, avg_us_hessian,
             denom, avg_wenzel_single,
             denom, avg_wenzel_hessian)
    plt.xticks(denom)
    plt.title('C Code vs Pytorch vs. Wenzel # It: 10')
    # legend
    plt.legend( ('Us-Single', 'Us-Hessian', 'Wenzel-Single', 'Wenzel-Hessian'),
            shadow=True, loc=(0.01, 0.48), handlelength=1.5, fontsize=16)
    plt.xlabel(function)
    plt.savefig('results/graph_{}.png'.format(func_num))
    plt.clf()

def function_generator(degree, variables, terms, input_string):
    def gen_polynomial(select_deg, append_term, select_var):
        for deg in range(0, select_deg-1):
            append_term += select_var + ' * '
        append_term += select_var
        return append_term


    op = [' + ', ' - ', ' * ', ' / ']
#     paranthesis = ['']
    blocks = random.randint(1,1)
    

    append_term = ''
    for b in range(blocks):

        select_deg = random.randint(1,degree)
        select_var = random.choice(variables)
        # fix this
#         select_paranthesis = random.choice(paranthesis)

        
        if b==0:
            append_term += gen_polynomial(select_deg, append_term, select_var)
        else:
            append_term = append_term + ' * '+gen_polynomial(select_deg, '', select_var)

    select_op = random.choice(op)
    
    if len(input_string)==0:
        input_string.append('('+append_term+')')
    else:
        input_string.append(select_op + '('+ append_term+')')

    if len(input_string) == terms:
        final_string = ''.join(input_string)  
        return final_string
    else:          
        return function_generator(degree, variables, terms, input_string)



if __name__ == "__main__":
    import random, string
    functions = []
    alphabets = list(string.ascii_lowercase)
    alphabets.remove('i')

    for k in range(2,11):
        temp = [function_generator(k,alphabets[0:5],20,[]), alphabets[0:5]]
        print(k)
        print(temp)
        functions.append(temp)

    print(functions)
    # functions = [
    #     [   , []]
    #     # ["(a*a+b*b+c*c+d*d)*(1+1/((a*d-b*c)*(a*d-b*c*e*f*g*h*j*k*l*m*n*o*p*q*r*s*t*u*v*w*x*y*z)))",["a","b","c","d","e","f","g","h","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]],
    #     # ["(a*a+b*b+c*c+d*d)*(1+1/((a*d-b*c)*(a*d-b*c)))",["a","b","c","d"]],
    #     # ["((k*k+3*k)-k/4)/k+k*k*k*k+k*k*(22/7*k)+k*k*k*k*k*k*k*k*k*j", ["k", "j"]],
    #     # ["((k*k+3*k)-k/4)/k+k*k*k*k+k*k*(22/7*k)+k*k*k*k*k*k*k*k*k", ["k"]],
    #     # ["sin(k) + cos(k) + pow(k, 2)", ["k"] ]
    # ]

    INPUT_FILENAME = 'utils/functions.c'
    UTILS_FILENAME = 'utils/windows_utils.c'
    OUTPUT_FILENAME = 'utils/output.txt'
    NUMPY_PARAMS_FILENAME = "utils/params.npy"
    PARAMS_FILENAME = 'utils/params.txt'
    PYTORCH_FILENAME = "utils/pytorch.py"
    PYTORCH_OUTPUT = "utils/pytorch_output.txt"
    INIT_NUM_PARAMS = 10
    num_vars = len(functions[0][1])
    NUM_ITERATIONS = 10
    NUM_THREADS_PYTORCH = 1
    RUN_C = True
    RUN_ISPC = False
    REVERSE = False
    SECOND_DER = True

    # cleanup()

    # raw_compare_file = open("results/raw_compare.txt", "w+")

    for func_num, func in enumerate(functions):

        avg_us_single = []
        avg_us_hessian = []
        avg_pytorch = []
        avg_wenzel_single = []
        avg_wenzel_hessian = []
        denom = []
        num_params = INIT_NUM_PARAMS

        # generate and compile our code
        us_utils.generate_function_c_file(func_num, functions, INPUT_FILENAME)
        us_utils.generate_derivatives_c_file(func_num, functions, INPUT_FILENAME, RUN_C, derivatives_filename="ders_single", reverse=REVERSE, second_der=False)
        us_utils.compile_ours(RUN_C, runnable_filename="runnable_single", utils_filename=UTILS_FILENAME, derivatives_filename="ders_single")

        us_utils.generate_derivatives_c_file(func_num, functions, INPUT_FILENAME, RUN_C, derivatives_filename="ders_hessian", reverse=REVERSE, second_der=True)
        us_utils.compile_ours(RUN_C, runnable_filename="runnable_hessian", utils_filename=UTILS_FILENAME, derivatives_filename="ders_hessian")

        while num_params <= 100000:

            print(num_params)

            # generate parameters
            params = generate_params(num_params, func_num)
            print_param_to_file(params)

            # generate pytorch file
            # pytorch_utils.generate_pytorch_file(func_num, num_params, functions)

            # generate and compile wenzel code
            # generate_enoki_file(func_num, num_params)
            # compile_enoki()
            wenzel_utils.generate_wenzel_file(func_num, num_params, functions, PARAMS_FILENAME, "single")
            wenzel_utils.compile_wenzel("single")
            wenzel_utils.generate_wenzel_file(func_num, num_params, functions, PARAMS_FILENAME, "hessian")
            wenzel_utils.compile_wenzel("hessian")

            # initialize arrays for run
            our_times_single = []
            our_times_hessian = []
            # py_times = []
            wenzel_times_single = []
            wenzel_times_hessian = []
            # enoki_times = []

            for i in range(NUM_ITERATIONS):
                # pytorch = pytorch_utils.run_pytorch()
                ours_single = us_utils.run_ours(functions[func_num], num_params, functions, PARAMS_FILENAME, output_filename="us_output_single.txt", runnable_filename="runnable_single")
                ours_hessian = us_utils.run_ours(functions[func_num], num_params, functions, PARAMS_FILENAME, output_filename="us_output_hessian.txt", runnable_filename="runnable_hessian")
                # enoki = run_enoki()
                wenzel_single = wenzel_utils.run_wenzel("single")
                wenzel_double = wenzel_utils.run_wenzel("hessian")

                # for j in range(len(ours[0])):
                #     assert math.isclose(float(pytorch[0][j]), float(wenzel[0][j]), abs_tol=10**-1)
                #     assert math.isclose(float(wenzel[0][j]), float(ours[0][j]), abs_tol=10**-1)
                    # assert math.isclose(float(ours[0][j]), float(enoki[0][j]), abs_tol=10**-1)
                our_times_single.append(float(ours_single[1]))
                our_times_hessian.append(float(ours_hessian[1]))
                # py_times.append(float(pytorch[1]))
                # enoki_times.append(float(enoki[1]))
                wenzel_times_single.append(float(wenzel_single[1]))
                wenzel_times_hessian.append(float(wenzel_double[1]))

            # print for debug purposes
            print("Parameters: ", params[:10])
            print("Snapshot of Our Single Results:", ours_single[0][: 10])
            print("Snapshot of Wenzel Single Results:", wenzel_single[0][: 10])
            print("Snapshot of Our Hessian Results:", ours_hessian[0][: 10])
            print("Snapshot of Wenzel Hessian Results:", wenzel_double[0][: 10])
            # print("Snapshot of Pytorch results: ", pytorch[0][: 10])
            # print("Snapshot of Wenzel results: ", wenzel[0][: 10])
            # print("Snapshot of Enoki results: ", enoki[0][: 10])

            # get the average time
            avg_us_single.append(sum(our_times_single) / len(our_times_single))
            avg_us_hessian.append(sum(our_times_hessian) / len(our_times_hessian))
            # avg_pytorch.append(sum(py_times) / len(py_times))
            # avg_enoki.append(sum(enoki_times) / len(enoki_times))
            avg_wenzel_single.append(sum(wenzel_times_single) / len(wenzel_times_single))
            avg_wenzel_hessian.append(sum(wenzel_times_hessian) / len(wenzel_times_hessian))
            denom.append(num_params)

            if num_params < 10000:
                num_params += 2000
            elif num_params > 10000 and num_params < 1000000:
                num_params = num_params + 10000
            else:
                num_params = num_params + 100000
        # print("Avg Us: " + str(avg_us))
        # print("Avg Pytorch: " + str(avg_pytorch))
        # print("Avg Enoki: " + str(avg_enoki))
        # print("Avg Wenzel: " + str(avg_wenzel))

        # final_compare = functions[func_num][0] + ": Wenzel -- " + str(avg_wenzel[-1]/avg_us[-1]) + "x PyTorch: " + str(avg_pytorch[-1]/avg_us[-1]) + "x\n"
        # raw_compare_file.write(final_compare)

        generate_graph(avg_us_single, avg_us_hessian, avg_wenzel_single, avg_wenzel_hessian, denom, func_num, functions[func_num][0])

    # raw_compare_file.close()
  
