import matplotlib.pyplot as plt
import numpy as np
import os
import json
import re


fontsize = 40
markersize = 20
linewidth = 3
num_params_list = [10, 2010, 4010, 6010, 8010, 10010, 20010, 30010, 40010]


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [atoi(c) for c in re.split(r'(\d+)', text)]


def convert_files_to_lists(file_location):
    wenzel_times_hess_static = {}
    us_times_hess = {}
    pytorch_hess_times = {}
    tapenade_hess_times = {}

    functions = []

    wenzel_hess_static_max = []
    tapenade_hess_max = []
    us_max_hess = []
    pytorch_max_hess = []

    with open(file_location) as json_data:
        data = json.load(json_data)

        for key in sorted(data):
            pytorch_hess_times[key] = []
            wenzel_times_hess_static[key] = []
            us_times_hess[key] = []
            tapenade_hess_times[key] = []
            functions.append(key)

            for num_params in num_params_list:
                num_params_str = str(num_params)
                wenzel_times_hess_static[key].append(
                    data[key][num_params_str]['wenzel_static'])
                tapenade_hess_times[key].append(
                    data[key][num_params_str]['tapenade'])
                us_times_hess[key].append(data[key][num_params_str]['us'])
                pytorch_hess_times[key].append(
                    data[key][num_params_str]['pytorch'])

            wenzel_hess_static_max.append(wenzel_times_hess_static[key][-1])
            tapenade_hess_max.append(tapenade_hess_times[key][-1])
            us_max_hess.append(us_times_hess[key][-1])
            pytorch_max_hess.append(pytorch_hess_times[key][-1])
    return us_times_hess, wenzel_times_hess_static, tapenade_hess_times, pytorch_hess_times, \
        functions, num_params_list, \
        us_max_hess, wenzel_hess_static_max, tapenade_hess_max, pytorch_max_hess


def generate_four_graph(avg_us, avg_wenzel_static, avg_tapenade, avg_pytorch, denom, num_vars):
    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(denom, avg_us, color='#130f40', markersize=50, linewidth=5)
    ax.plot(denom, avg_pytorch, color='#ff7979', linewidth=linewidth)
    ax.plot(denom, avg_wenzel_static, color='#badc58', linewidth=linewidth)
    ax.plot(denom, avg_tapenade, color='#7ed6df', linewidth=linewidth)
    ax.set_yscale('log')
    plt.ylim(1.e-05, 1.e+03)
    plt.xlim(2010, 40010)
    plt.setp(ax.get_xticklabels(), fontsize=20)
    plt.setp(ax.get_yticklabels(), fontsize=20)
    # legend
    plt.margins(0, 0)
    plt.savefig('./tests/results/hess/graphs/non-random/full/{}_function_hess_g++9.pdf'.format(num_vars), bbox_inches='tight',
                pad_inches=0)
    plt.clf()


file_location = "./tests/results/hess/json/non-random/full_results.json"

us_times_hess, wenzel_times_hess_static, tapenade_times_hess, pytorch_times_hess, \
    functions, num_params, \
    us_max_hess, wenzel_hess_static_max, tapenade_max_times, pytorch_max_hess = convert_files_to_lists(
        file_location)

for i, label in enumerate(functions):
    # print(wenzel_times_hess_static[label])
    generate_four_graph(us_times_hess[label], wenzel_times_hess_static[label],
                        tapenade_times_hess[label], pytorch_times_hess[label], num_params, i)
