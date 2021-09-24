import numpy as np
import torch
import time
import os
os.environ['NPY_MKL_FORCE_INTEL'] = 'GNU'

num_params = 90010
J = torch.tensor(np.load('./tests/utils/numpy_params/function_9_param_J.npy'), requires_grad=True, dtype=torch.float)
T = torch.tensor(np.load('./tests/utils/numpy_params/function_9_param_T.npy'), requires_grad=True, dtype=torch.float)
k = torch.tensor(np.load('./tests/utils/numpy_params/function_9_param_k.npy'), requires_grad=True, dtype=torch.float)
a = torch.tensor(np.load('./tests/utils/numpy_params/function_9_param_a.npy'), requires_grad=True, dtype=torch.float)
h = torch.tensor(np.load('./tests/utils/numpy_params/function_9_param_h.npy'), requires_grad=True, dtype=torch.float)
v = torch.tensor(np.load('./tests/utils/numpy_params/function_9_param_v.npy'), requires_grad=True, dtype=torch.float)
s = torch.tensor(np.load('./tests/utils/numpy_params/function_9_param_s.npy'), requires_grad=True, dtype=torch.float)
r = torch.tensor(np.load('./tests/utils/numpy_params/function_9_param_r.npy'), requires_grad=True, dtype=torch.float)
N = torch.tensor(np.load('./tests/utils/numpy_params/function_9_param_N.npy'), requires_grad=True, dtype=torch.float)
e = torch.tensor(np.load('./tests/utils/numpy_params/function_9_param_e.npy'), requires_grad=True, dtype=torch.float)
torch.set_num_threads(1)
y = (4*4*4*4*4*4*4*4*4*4*((J * (1 - J))*(T * (1 - T))*(k * (1 - k))*(a * (1 - a))*(h * (1 - h))*(v * (1 - v))*(s * (1 - s))*(r * (1 - r))*(N * (1 - N))*(e * (1 - e)))).sum()
start_time_pytorch = time.time()
y.backward()
J.grad
T.grad
k.grad
a.grad
h.grad
v.grad
s.grad
r.grad
N.grad
e.grad

end_time_pytorch = time.time()
runtime = (end_time_pytorch - start_time_pytorch)
print(str(runtime))
J_list = J.grad.tolist()
T_list = T.grad.tolist()
k_list = k.grad.tolist()
a_list = a.grad.tolist()
h_list = h.grad.tolist()
v_list = v.grad.tolist()
s_list = s.grad.tolist()
r_list = r.grad.tolist()
N_list = N.grad.tolist()
e_list = e.grad.tolist()

for i in range(num_params):
	print(str(J_list[i]))
	print(str(T_list[i]))
	print(str(k_list[i]))
	print(str(a_list[i]))
	print(str(h_list[i]))
	print(str(v_list[i]))
	print(str(s_list[i]))
	print(str(r_list[i]))
	print(str(N_list[i]))
	print(str(e_list[i]))
