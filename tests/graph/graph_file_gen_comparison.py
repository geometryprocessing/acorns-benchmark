import matplotlib.pyplot as plt
import numpy as np
import os
import json
import re


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [atoi(c) for c in re.split(r'(\d+)', text)]


def convert_files_to_lists(us_file_location, tape_file):
    forward = []
    reverse = []
    tapenade = []
    with open(us_file_location) as json_data:
        data = json.load(json_data)
        for key in data:
            print(key)
            forward.append(data[key]['false']['file_gen_time'])
            reverse.append(data[key]['true']['file_gen_time'])

    with open(tape_file) as json_data:
        data = json.load(json_data)
        for key in data:
            print(key)
            tapenade.append(data[key]['false']['file_gen_time'])
    return forward, reverse, tapenade, range(1, 25)


def get_speedup_list(time_list):
    speedup_list = []
    single_thread_time = time_list[0]
    for time in time_list[1:]:
        speedup_list.append(float(single_thread_time) / float(time))
    return speedup_list


def generate_two_graph(first, second, first_label, second_label, suffix, denom):
    plt.plot(denom, first, color='#1abc9c', linestyle='dashed',  markersize=7)
    plt.plot(denom, second, color='#f1c40f',
             linestyle='dashed', markersize=7)
    # legend
    plt.legend((first_label, second_label),
               shadow=False, fontsize=10, frameon=False)
    plt.margins(0, 0)
    plt.savefig('./tests/results/hess/graphs/file_gen_graph_{}.pdf'.format(suffix), bbox_inches='tight',
                pad_inches=0)
    plt.clf()



forward, reverse, tapenade, denom = convert_files_to_lists(
    "./tests/results/hess/json/file_gen/full_results_file_gen-2020-06-24-22:47:09.json", 
    "./tests/results/hess/json/file_gen/full_results_file_gen_tapenade-2020-06-24-23:16:30.json")

print(forward)

generate_two_graph(forward, reverse, 'Us (Forward)', 'Us (Reverse)', 'us', denom)
generate_two_graph(reverse, tapenade, 'Us (Reverse)', 'Tapenade', 'tape', denom)