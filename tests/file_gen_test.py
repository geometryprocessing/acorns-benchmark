import sys
import math
import matplotlib.pyplot as plt
import torch
from timeit import default_timer as timer
import os
import json
from subprocess import PIPE, run
import numpy as np
import shutil
from datetime import datetime
import multiprocessing as mp
import time

sys.path.append('./acorns')
import forward_diff

sys.path.append('./tests/python_test_utils')
import random, string
import us_utils
import generate_function

def generate_vars_str(vars):
    vars_str = ""
    for i, var in enumerate(vars):
        vars_str += "double {}".format(var)
        if (i != len(vars) - 1):
            vars_str += ", "
    return vars_str

import random, string
functions = []
alphabets = list(string.ascii_lowercase)
alphabets.remove('i')
# alphabets.remove('p')

for k in range(1, 25):
    function = generate_function.generate_simple(k)
    functions.append(function)
    print(function)

bool_vals = [True, False]
num_iterations = 10

output = {}

# num_params = 10

if not os.path.exists('output'):
    os.mkdir('output')

for func_num, func in enumerate(functions):

    num_vars = len(func[1])
    vars_str = generate_vars_str(func[1])

    output[num_vars] = {}

    avg_us = []
    denom = []

    c_function = "int function_test({}){{ \
        int energy = {}; \
        return 0; \
    }}".format(vars_str, func[0])

    print(c_function)

    for bool_val in bool_vals:

        times = []
        for i in range(num_iterations):
            start_time_pytorch = time.time()

            forward_diff.autodiff(c_function, 'energy', func[1], func = 'function_test', output_filename = 'output/test_grad',
                output_func = 'compute_grad', reverse_diff=bool_val, second_der=True)
            # generate and compile our code
            end_time_pytorch = time.time()
            file_gen_time = (end_time_pytorch - start_time_pytorch)
            times.append(file_gen_time)

        avg_time = sum(times) / len(times)

        output[num_vars][bool_val] = {
            "file_gen_time": avg_time
        }
    
file_suffix = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
output_file = open('./tests/results/hess/full_results_file_gen-{}.json'.format(file_suffix), "w+")
output_file.write(json.dumps(output, indent=4))
output_file.close()