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
import tapenade_utils
import us_utils
import wenzel_utils
import pytorch_utils
import enoki_utils
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

for func_num, func in enumerate(functions):

    num_vars = len(func[1])
    vars_str = generate_vars_str(func[1])

    output[num_vars] = {}

    tapenade_utils.generate_function_c_file(
            func_num, functions, './tests/utils/tapenade_func.c')

    for bool_val in bool_vals:

        times = []
        for i in range(num_iterations):
            start_time_tapenade_file_gen = time.time()
            tapenade_utils.generate_hessian_c_file(func_num)
            end_time_tapenade_file_gen = time.time()
            tapenade_file_gen_time = (end_time_tapenade_file_gen - start_time_tapenade_file_gen)
            times.append(tapenade_file_gen_time)

        avg_time = sum(times) / len(times)
        print("Num Vars: {}, Time: {}".format(num_vars, avg_time))

        output[num_vars][bool_val] = {
            "file_gen_time": avg_time
        }
    
file_suffix = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
output_file = open('./tests/results/hess/full_results_file_gen_tapenade-{}.json'.format(file_suffix), "w+")
output_file.write(json.dumps(output, indent=4))
output_file.close()