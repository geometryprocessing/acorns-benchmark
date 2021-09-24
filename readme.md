### Readme

This contains all of the code used to generate JSON benchmarks and graphs for ACORNS: An easy-to-use Code Generator for Gradients and Hessians

### About acorns

Home: https://github.com/deshanadesai/acorns

Package license: MIT

Feedstock license: BSD 3-Clause

Summary: An easy-to-use Code Generator for Gradients and Hessians

ACORNS is an algorithm for automatic differention of algorithms written in a subset of C99 code and its efficient implementation as a Python script.

### Prerequisites

In order to run the benchmarking you need Pytorch installed, Adept installed, Java1.8 or higher and GCC9.
- To intall PyTorch simply using pip you can simply type `pip install torch`
- To install Adept follow the instructions found [here](http://www.met.reading.ac.uk/clouds/adept/documentation.html)
  -   *NOTE*: Adept has been installed ONLY with `./configure` and the scripts rely on the location of the binaries.
- On a mac you can find a working version of GCC9 with Homebrew and install it with `brew install gcc@9`
- In order to graph you must have `matplotlib` installed which can be installed through pip.

### Benchmarking Overview

This hosts all of the code used to generate the data and graphs for [ACORNS](https://arxiv.org/abs/2007.05094)
There are 5 main functions that generate the data:
1. `tests/updated_test_suite.py` - This runs ACORNS against PyTorch, Adept, Mitsuba, Enoki and Tapenade with respect to 2 hardcoded functions:
  a. `((k*k+3*k)-k/4)/k+k*k*k*k+k*k*(22/7*k)+k*k*k*k*k*k*k*k*k`
  b. `sin(k) + cos(k) + pow(k, 2)`

this returns the gradient of all of them and outputs the results in `./tests/results/grad/full_results-{TIMESTAMP}.json`

2. `tests/updated_test_suite_random.py` This runs ACORNS for the gradient against PyTorch, Adept, Mitsuba, Enoki and Tapenade with respect to 10 different functions, each one having increasing variables (from 1 to 10)
this returns the gradient of all of them and outputs the results in `./tests/results/grad/full_results_random-{TIMESTAMP}.json`

3. `tests/updated_hessian_test_suite.py` This runs ACORNS for the hessian against Mitsuba, PyTorch and Tapenade for the functions given in (1)
this returns the gradient of all of them and outputs the results in `./tests/results/hess/full_results_hessian-{TIMESTAMP}.json`

4. `tests/updated_hessian_test_suite_random.py` This runs ACORNS for the hessian against Mitsuba, PyTorch and Tapenade with respect to 10 different functions, each one having increasing variables (from 1 to 10)
this returns the gradient of all of them and outputs the results in `./tests/results/hess/full_results_hessian-{TIMESTAMP}.json`
5. `tests/parallel_test_suite.py` This runs ACORNS with OpenMP across threads increasing from 1 to 25
this returns the gradient of all of them and outputs the results in `./tests/results/hess/full_results_parallel-{TIMESTAMP}.json`

### Graphing

We graph our runtimes against all of the competitors in `./tests/graph/` folder. Right now these files are hardcoded to accept JSON from our latest runs which were output from the scritps in Benchmarking 
1. To graph Gradient Hardcoded run `./tests/graph/gradient_non_random_graphs-g++9.py`
2. To graph Gradient Random run `./tests/graph/gradient_random_graphs-g++9.py`
3. To graph Hessian Hardcoded run `./tests/graph/hessian_non_random_graphs-g++9.py`
4. To graph Hessian Hardcoded run `./tests/graph/hessian_random_graphs-g++9.py`
5. To graph how ACORNS scales with respect to threads run `./tests/graph/parallel_graphs.py`

### Real World Example

In our paper we outline how we used this in a PolyFEM application. This was very complex and the C code was too big to include here. As such we simple calculated the times in JSON which can be found in the `./tests/complex/data`

1. To graph file generation time run `./tests/complex/graph_file_gen.py`
2. To graph file sizes run `./tests/complex/graph_file_sizes.py`
3. To graph how PolyFEM runs with respect to file splitting run `./tests/complex/graph/graph_runs.py`
  



