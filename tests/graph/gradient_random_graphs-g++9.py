import matplotlib.pyplot as plt
import json
import re

num_params_list = [10, 2010, 4010, 6010, 8010, 10010,
                   20010, 30010, 40010, 50010, 60010, 70010, 80010, 90010]

fontsize = 40
markersize = 20
linewidth = 3


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [atoi(c) for c in re.split(r'(\d+)', text)]


def convert_files_to_lists(file_location, adept_file_location):
    wenzel_static_times = {}
    wenzel_dynamic_times = {}
    enoki_times = {}
    pytorch_times = {}
    us_times = {}
    tapenade_times = {}
    adept_times = {}
    functions = []

    wenzel_static_max = []
    wenzel_dynamic_max = []
    enoki_max = []
    pytorch_max = []
    tapenade_max = []
    us_max = []
    adept_max = []

    with open(file_location) as json_data:
        with open(adept_file_location) as adept_json_data:
            data = json.load(json_data)
            data_list = sorted(data)
            adept_data = json.load(adept_json_data)
            adept_data_list = sorted(adept_data)
            print(data_list)
            print(adept_data_list)
            for i, key in enumerate(sorted(data)):
                wenzel_static_times[i] = []
                wenzel_dynamic_times[i] = []
                enoki_times[i] = []
                pytorch_times[i] = []
                us_times[i] = []
                tapenade_times[i] = []
                adept_times[i] = []
                functions.append(i)

                for num_params in num_params_list:
                    num_params_str = str(num_params)
                    wenzel_static_times[i].append(
                        adept_data[adept_data_list[i]][num_params_str]['wenzel_static'])
                    wenzel_dynamic_times[i].append(
                        adept_data[adept_data_list[i]][num_params_str]['wenzel_dynamic'])
                    enoki_times[i].append(data[data_list[i]][num_params_str]['enoki'])
                    us_times[i].append(adept_data[adept_data_list[i]][num_params_str]['us'])
                    pytorch_times[i].append(adept_data[adept_data_list[i]][num_params_str]['pytorch'])
                    tapenade_times[i].append(
                        data[data_list[i]][num_params_str]['tapenade'])
                    adept_times[i].append(adept_data[adept_data_list[i]][num_params_str]['adept'])

                # print("{}:{} = {}".format(key, num_params, us_times[key][-1]))

                wenzel_static_max.append(wenzel_static_times[i][-1])
                wenzel_dynamic_max.append(wenzel_dynamic_times[i][-1])
                enoki_max.append(enoki_times[i][-1])
                pytorch_max.append(pytorch_times[i][-1])
                us_max.append(us_times[i][-1])
                tapenade_max.append(tapenade_times[i][-1])
                adept_max.append(adept_times[i][-1])
    return wenzel_static_times, wenzel_dynamic_times, enoki_times, pytorch_times, us_times, \
        tapenade_times, adept_times, functions, num_params_list, wenzel_static_max, wenzel_dynamic_max, \
            enoki_max, pytorch_max, us_max, tapenade_max, adept_max


def generate_two_graph(avg_us, avg_them, denom, label, num_vars):
    plt.plot(denom, avg_us, color='#130f40', linestyle='dashed',  markersize=7)
    plt.plot(denom, avg_them, color='#f1c40f',
             linestyle='dashed', markersize=7)
    # legend
    plt.xlabel('Parameters', fontfamily='monospace')
    plt.ylabel('Time (s)', fontfamily='monospace')
    plt.legend(('Us', label),
               shadow=False, fontsize=fontsize, frameon=False)
    plt.margins(0, 0)
    plt.savefig('./tests/results/grad/graphs/g++9/non-random/graph_{}_{}.pdf'.format(label, num_vars), bbox_inches='tight',
                pad_inches=0)
    # plt.savefig('./tests/complex/graphs/graph_by_128_speedup.pdf')
    plt.clf()


def generate_full_graph(avg_us, avg_pytorch, avg_wenzel_static, avg_enoki, avg_tapenade, avg_adept, denom, num_vars):
    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(denom, avg_us, color='#130f40', markersize=50, linewidth=7)
    ax.plot(denom, avg_pytorch, color='#ff7979', linewidth=linewidth)
    ax.plot(denom, avg_wenzel_static, color='#badc58', linewidth=linewidth)
    ax.plot(denom, avg_enoki, color='#e056fd', linewidth=linewidth)
    ax.plot(denom, avg_tapenade, color='#7ed6df', linewidth=linewidth)
    ax.plot(denom, avg_adept, color='#DA6A92', linewidth=linewidth)
    ax.set_yscale('log')
    plt.setp(ax.get_xticklabels(), fontsize=20)
    plt.setp(ax.get_yticklabels(), fontsize=20)
    plt.ylim(1.e-05, 1.e-01)
    plt.xlim(2010, 90010)
    plt.legend(('ACORNS', 'Pytorch', 'Mitsuba', 'Enoki', 'Tapenade', 'Adept'),
               shadow=False, fontsize=fontsize, frameon=False)
    plt.margins(0, 0)
    plt.savefig('./results/grad/graphs/g++9/random/graph_{}_full_grad_g++9.pdf'.format(num_vars), bbox_inches='tight',
                pad_inches=0)
    plt.clf()

def generate_max_graph(avg_us, avg_pytorch, avg_wenzel_static, avg_enoki, avg_tapenade, avg_adept, denom):
    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(denom, avg_us, color='#130f40', markersize=50, linewidth=7)
    ax.plot(denom, avg_pytorch, color='#ff7979', linewidth=linewidth)
    ax.plot(denom, avg_wenzel_static, color='#badc58', linewidth=linewidth)
    ax.plot(denom, avg_enoki, color='#e056fd', linewidth=linewidth)
    ax.plot(denom, avg_tapenade, color='#7ed6df', linewidth=linewidth)
    ax.plot(denom, avg_adept, color='#DA6A92', linewidth=linewidth)
    ax.set_yscale('log')
    plt.ylim(1.e-04, 1.e-01)
    plt.setp(ax.get_xticklabels(), fontsize=20)
    plt.setp(ax.get_yticklabels(), fontsize=20)
    # legend
    plt.legend(('ACORNS', 'Pytorch', 'Mitsuba', 'Enoki', 'Tapenade', 'Adept'),
               shadow=False, fontsize=fontsize, frameon=False)
    plt.margins(0, 0)
    plt.savefig('./results/grad/graphs/g++9/random/graph_max_grad_g++9.pdf', bbox_inches='tight',
                pad_inches=0)
    plt.clf()

#results/grad/full_results-2021-09-13-13:10:02.json

wenzel_static_times, wenzel_dynamic_times, enoki_times, pytorch_times, us_times, tapenade_times, adept_times, \
    functions, num_params, wenzel_static_max, wenzel_dynamic_max, enoki_max, pytorch_max, \
        us_max, tapenade_max, adept_max = convert_files_to_lists(
    "./results/grad/json/random/full_results_random-2020-04-21-20:37:58.json",
    "./results/grad/full_results_random-2021-09-13-18:07:55.json")

for i, label in enumerate(functions):
    # print(us_times[label])
    generate_full_graph(us_times[i], pytorch_times[i], wenzel_static_times[i],
                        enoki_times[i], tapenade_times[i], adept_times[i], num_params, i)
    # generate_full_graph_without_dynamic(us_times[label], pytorch_times[label], wenzel_static_times[label], enoki_times[label], tapenade_times[label], num_params, label, 'Wenzel', i)

generate_max_graph(us_max, pytorch_max, wenzel_static_max,
                   enoki_max, tapenade_max, adept_max, range(1, 11))
