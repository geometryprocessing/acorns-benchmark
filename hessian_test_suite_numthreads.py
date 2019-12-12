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
# import wenzel_utils

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

def generate_graph(avg_us_single, avg_us_hessian, denom, func_num, function):
    plt.figure(1)
    plt.subplot(211)
    plt.plot(denom, avg_us_single,
             denom, avg_us_hessian)
    plt.xticks(denom)
    plt.title('C Code vs Pytorch vs. Wenzel # It: 10')
    # legend
    plt.legend( ('Us-Single', 'Us-Parallel'),
            shadow=True, loc=(0.01, 0.48), handlelength=1.5, fontsize=16)
    plt.xlabel(function)
    plt.savefig('results/graph_{}.png'.format(func_num))
    plt.clf()



if __name__ == "__main__":
    import ast
    import os
    y_op_2 = []
    y_op_3 = []
    y_op_4 = []

    start = 50
    stop = 250
    ts = 50

    for i in range(start, stop, ts):

    # for i in range(5,50,5):
        os.system('python3 function_generator.py 5 '+str(i))
        f = open('generated_function.txt')
        function_string = ast.literal_eval(f.read())
        f.close()

        functions = [function_string]

        INPUT_FILENAME = 'utils/functions.c'
        UTILS_FILENAME = 'utils/windows_utils.c'
        OUTPUT_FILENAME = 'utils/output.txt'
        NUMPY_PARAMS_FILENAME = "utils/params.npy"
        PARAMS_FILENAME = 'utils/params.txt'
        PYTORCH_FILENAME = "utils/pytorch.py"
        PYTORCH_OUTPUT = "utils/pytorch_output.txt"
        INIT_NUM_PARAMS = 100000
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
            avg_us_parallel_2 = []
            avg_us_parallel_3 = []
            avg_us_parallel_4 = []
            avg_pytorch = []
            avg_wenzel_single = []
            avg_wenzel_hessian = []
            denom = []
            num_params = INIT_NUM_PARAMS

            # generate and compile our code
            us_utils.generate_function_c_file(func_num, functions, INPUT_FILENAME)
            print('creating derivative file')
            us_utils.generate_derivatives_c_file(func_num, functions, INPUT_FILENAME, RUN_C, derivatives_filename="hessian_seq", reverse=REVERSE, second_der=True, parallel = False)
            us_utils.compile_ours(RUN_C, runnable_filename="runnable_hessian", utils_filename=UTILS_FILENAME, derivatives_filename="hessian_seq")
            
            print('creating derivative file')

            us_utils.generate_derivatives_c_file(func_num, functions, INPUT_FILENAME, RUN_C, derivatives_filename="hessian_par", reverse=REVERSE, second_der=True, parallel =  True)
            us_utils.compile_ours(RUN_C, runnable_filename="runnable_hessian_parallel", utils_filename=UTILS_FILENAME, derivatives_filename="hessian_par")

            # while num_params <= 100000:

            print(num_params)

            # generate parameters
            params = generate_params(num_params, func_num)
            print_param_to_file(params)



            # initialize arrays for run
            our_times_seq = []
            our_times_par_2 = []
            our_times_par_3 = []
            our_times_par_4 = []


            for i in range(NUM_ITERATIONS):
                # pytorch = pytorch_utils.run_pytorch()

                print('starting sequential diff')
                os.environ["OMP_NUM_THREADS"] = '1'
                ours_single = us_utils.run_ours(functions[func_num], num_params, functions, PARAMS_FILENAME, output_filename="us_output_seq.txt", runnable_filename="runnable_hessian")                
                

                print('starting parallel diff for numthreads 2')
                os.environ["OMP_NUM_THREADS"] = '2'
                ours_hessian_2 = us_utils.run_ours(functions[func_num], num_params, functions, PARAMS_FILENAME, output_filename="us_output_par.txt", runnable_filename="runnable_hessian_parallel")
                

                print('starting parallel diff for numthreads 3')
                os.environ["OMP_NUM_THREADS"] = '3'

                ours_hessian_3 = us_utils.run_ours(functions[func_num], num_params, functions, PARAMS_FILENAME, output_filename="us_output_par.txt", runnable_filename="runnable_hessian_parallel")

                print('starting parallel diff for numthreads 4')
                os.environ["OMP_NUM_THREADS"] = '4'
                ours_hessian_4 = us_utils.run_ours(functions[func_num], num_params, functions, PARAMS_FILENAME, output_filename="us_output_par.txt", runnable_filename="runnable_hessian_parallel")



                our_times_seq.append(float(ours_single[1]))
                our_times_par_2.append(float(ours_hessian_2[1]))
                our_times_par_3.append(float(ours_hessian_3[1]))
                our_times_par_4.append(float(ours_hessian_4[1]))


            # print for debug purposes
            print("Parameters: ", params[:10])
            print("Snapshot of Our Sequential Results:", ours_single[0][-10:])
            print("size of our sequqnetial results: ",len(ours_single[0]))
            # print("Snapshot of Wenzel Single Results:", wenzel_single[0][: 10])


            print("Snapshot of Our parallel Results 2:", ours_hessian_2[0][-10:])
            print("size of our parallel results: ",len(ours_hessian_2[0]))

            print("Snapshot of Our parallel Results 3:", ours_hessian_3[0][-10:])
            print("size of our parallel results: ",len(ours_hessian_3[0]))  

            print("Snapshot of Our parallel Results 4:", ours_hessian_4[0][-10:])
            print("size of our parallel results: ",len(ours_hessian_4[0]))                      

            # get the average time
            avg_us_single.append(sum(our_times_seq) / len(our_times_seq))
            avg_us_parallel_2.append(sum(our_times_par_2) / len(our_times_par_2))
            avg_us_parallel_3.append(sum(our_times_par_3) / len(our_times_par_3))
            avg_us_parallel_4.append(sum(our_times_par_4) / len(our_times_par_4))

            denom.append(num_params)
            


            # if num_params < 10000:
            #     num_params += 2000
            # elif num_params > 10000 and num_params < 1000000:
            #     num_params = num_params + 10000
            # else:
            #     num_params = num_params + 100000

            print("time: ")
            print(avg_us_single)
            print("parallel:")
            print(avg_us_parallel_4)

            speedup_2 = avg_us_single[-1]/avg_us_parallel_2[-1]
            speedup_3 = avg_us_single[-1]/avg_us_parallel_3[-1]
            speedup_4 = avg_us_single[-1]/avg_us_parallel_4[-1]
            print('speedup: ',speedup_4)
            y_op_2.append(speedup_2)
            y_op_3.append(speedup_3)
            y_op_4.append(speedup_4)
                

            # generate_graph(avg_us_single, avg_us_hessian, denom, func_num, functions[func_num][0])

        # raw_compare_file.close()
    print(y_op_2)
    print(y_op_3)
    print(y_op_4)
    plt.figure(1)
    plt.subplot(211)
    plt.plot(list(range(start, stop, ts)), y_op_2, label = 'num threads=2')
    plt.plot(list(range(start, stop, ts)), y_op_3, label = 'num threads=3')
    plt.plot(list(range(start, stop, ts)), y_op_4, label = 'num threads=4')
    plt.xticks(list(range(start, stop, ts)))
    plt.title('sequential vs parallel speedup')
    # legend
    plt.legend(loc="lower right")


    plt.xlabel('# of iterations = 10, # of params = 100k, constant # of variables (5), x = # of terms')
    plt.ylabel('speedup')
    plt.savefig('results/graph_parallel_numthreads.png')
    plt.clf()    
  
