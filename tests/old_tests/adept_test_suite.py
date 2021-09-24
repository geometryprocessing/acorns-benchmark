
import sys
import matplotlib.pyplot as plt
from timeit import default_timer as timer
import os
import json
from datetime import datetime

print(sys.path)

sys.path.append('tests/python_test_utils')
import adept_utils


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
    if os.path.exists(PARAMS_FILENAME):
        os.remove(PARAMS_FILENAME)
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


def generate_graph(avg_us, avg_pytorch, avg_wenzel, denom, func_num, function):
    plt.figure(1)
    plt.subplot(211)
    plt.plot(denom, avg_us,
             denom, avg_pytorch,
             denom, avg_wenzel)
    plt.xticks(denom)
    plt.title('C Code vs Pytorch vs. Wenzel # It: 10')
    # legend
    plt.legend(('Ours', 'Pytorch', 'Wenzel'),
               shadow=True, loc=(0.01, 0.48), handlelength=1.5, fontsize=16)
    plt.xlabel(function)
    plt.savefig('./tests/results/graph_{}.png'.format(func_num))
    plt.clf()


if __name__ == "__main__":
    functions = [
        ["sum(((k*k+3*k)-k/4)/k+k*k*k*k+k*k*(22/7*k)+k*k*k*k*k*k*k*k*k)", ["k"]],
        ["sum(sin(k)) + sum(cos(k)) + sum(pow(k, 2))", ["k"]]
    ]
    PARAMS_FILENAME = './tests/utils/params.txt'
    INIT_NUM_PARAMS = 10
    num_vars = len(functions[0][1])
    NUM_ITERATIONS = 10
    WENZEL_COMPILER_VERSION = ""

    output = {}

    for func_num, func in enumerate(functions):

        print(func)

        output[func[0]] = {}

        denom = []
        num_params = INIT_NUM_PARAMS

        while num_params <= 100000:

            # generate parameters
            params = generate_params(num_params, func_num)
            print_param_to_file(params)

            adept_utils.generate_adept_file(func_num, num_params, functions, PARAMS_FILENAME)
            adept_utils.compile_adept()

            # initialize arrays for run
            adept_times = []

            for i in range(NUM_ITERATIONS):
                adept = adept_utils.run_adept()

                print(f"Adept: {adept}")
                adept_times.append(float(wenzel_dynamic[1]))

            # print for debug purposes
            print("Parameters: ", params[:10])

            output[func[0]][num_params] = {
                "wenzel_static": (sum(wenzel_times_static) / len(wenzel_times_static)),
                "wenzel_dynamic": (sum(wenzel_times_dynamic) / len(wenzel_times_dynamic)),
                "flags": "-ffast-math -O3",
                "compiler_version": WENZEL_COMPILER_VERSION
            }

            denom.append(num_params)
            if num_params < 10000:
                num_params += 2000
            else:
                num_params = num_params + 10000

    file_suffix = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    output_file = open(
        './tests/results/grad/full_results-{}.json'.format(file_suffix), "w+")
    output_file.write(json.dumps(output, indent=4, sort_keys=True))
    output_file.close()
