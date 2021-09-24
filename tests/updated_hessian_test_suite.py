import sys
import math
import torch
from timeit import default_timer as timer
import os
import json
from subprocess import PIPE, run
import numpy as np
import shutil
from datetime import datetime

sys.path.append('tests/python_test_utils')

sys.path.append('acorns')

import us_utils
import wenzel_utils
import pytorch_utils
import tapenade_utils

tapenade = False


def generate_params(num_params, function_num):
    # , " which is: ", functions[function_num][0])
    print("Generating params for function_num", function_num)
    num_variables = len(functions[function_num][1])
    function_params = np.zeros(shape=(num_variables, num_params))
    for i, var in enumerate(functions[function_num][1]):
        variable_params = np.random.rand(num_params) * 10
        np.save("./tests/utils/numpy_params/function_{}_param_{}.npy".format(
            function_num, var), variable_params)
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
    if os.path.exists(OUTPUT_FILENAME):
        os.remove(OUTPUT_FILENAME)
    if os.path.exists(PARAMS_FILENAME):
        os.remove(PARAMS_FILENAME)

    if os.path.exists("./tests/hessian_test/utils"):
        folder = './tests/hessian/utils'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
    if os.path.exists("./tests/hessian/results"):
        folder = './tests/hessian/results'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)

if __name__ == "__main__":
    functions = [
        ["((k*k+3*k)-k/4)/k+k*k*k*k+k*k*(22/7*k)+k*k*k*k*k*k*k*k*k", ["k"]],
        ["sin(k) + cos(k) + pow(k, 2)", ["k"] ]
    ]

    INPUT_FILENAME = './tests/utils/hessian/functions.c'
    UTILS_FILENAME = './tests/utils/windows/windows_utils.c'
    OUTPUT_FILENAME = './tests/utils/hessian/us_output.txt'
    PARAMS_FILENAME = './tests/utils/hessian/params.txt'
    MAX_PARAMS = 50000
    INIT_NUM_PARAMS = 10
    WENZEL_COMPILER_VERSION = ""
    NUM_ITERATIONS = 10
    RUN_C = True

    RUNNABLE_TAPENADE = './tests/utils/runnable_tapenade_hess'
    TAPENADE_OUTPUT = './tests/utils/tapenade_output_hess.txt'
    output = {}

    for func_num, func in enumerate(functions):

        print(func[0])

        output[func[0]] = {}

        denom = []
        num_params = INIT_NUM_PARAMS

#         # generate and compile our code
        us_utils.generate_function_c_file(func_num, functions, INPUT_FILENAME)
        us_utils.generate_derivatives_c_file(func_num, functions, INPUT_FILENAME, RUN_C, derivatives_filename="./tests/utils/hessian/ders_hessian", reverse=False, second_der=True)
        us_utils.compile_ours(RUN_C, runnable_filename="./tests/utils/static_code/runnable_hessian", derivatives_filename="./tests/utils/hessian/ders_hessian")

        # generate and compile tapenade code
        if tapenade:
            tapenade_utils.generate_function_c_file(
                func_num, functions, './tests/utils/tapenade_func.c')
            tapenade_utils.generate_hessian_c_file(func_num)
            tapenade_utils.generate_runnable_tapenade_hess(
                func[1], len(func[1]), func_num)
            tapenade_utils.compile('./tests/utils/runnable_tapenade_hess')

        while num_params <= MAX_PARAMS:

            # generate parameters
            params = generate_params(num_params, func_num)
            print_param_to_file(params)

            # generate pytorch file
            pytorch_utils.generate_pytorch_hessian_file(
                func_num, num_params, functions)

            # generate and compile wenzel code static 
            wenzel_utils.generate_wenzel_file(func_num, num_params, functions, PARAMS_FILENAME, "hessian", True)
            wenzel_utils.compile_wenzel("hessian", True, compiler_version=WENZEL_COMPILER_VERSION)

            # initialize arrays for run
            our_times = []
            py_times = []
            wenzel_times_static = []
            tapenade_times = []

            for i in range(NUM_ITERATIONS):

                pytorch = pytorch_utils.run_pytorch_hessian()
                ours = us_utils.run_ours(
                    functions[func_num], num_params, functions, PARAMS_FILENAME, OUTPUT_FILENAME,   runnable_filename="./tests/utils/static_code/runnable_hessian")
                wenzel_static = wenzel_utils.run_wenzel("hessian", True)
                if tapenade:
                    tapenade = tapenade_utils.run_tapenade(functions[func_num], num_params, functions, PARAMS_FILENAME, TAPENADE_OUTPUT, RUNNABLE_TAPENADE)


                tapenade_times.append(float(tapenade[1]))
                our_times.append(float(ours[1]))
                py_times.append(float(pytorch[1]))
                wenzel_times_static.append(float(wenzel_static[1]))


            output[func[0]][num_params] = {
                "us": sum(our_times) / len(our_times),
                "pytorch": sum(py_times) / len(py_times),
                "wenzel_static": (sum(wenzel_times_static) / len(wenzel_times_static)),
                "tapenade": sum(tapenade_times) / len(tapenade_times) if tapenade else None,
                "flags": "-ffast-math -O3",
                "compiler_version": WENZEL_COMPILER_VERSION
            }

            denom.append(num_params)
            if num_params < 10000:
                num_params += 2000
            else:
                num_params = num_params + 10000


    file_suffix = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    output_file = open('./tests/results/hess/full_results_hessian-{}.json'.format(file_suffix), "w+")
    output_file.write(json.dumps(output, indent=4, sort_keys=True))
    output_file.close()
