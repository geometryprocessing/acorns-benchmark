import numpy as np
import torch
import time
import os
os.environ['NPY_MKL_FORCE_INTEL'] = 'GNU'

num_params = 20010
k = torch.tensor(np.load('./tests/utils/numpy_params/function_0_param_k.npy'), requires_grad=True, dtype=torch.float)
torch.set_num_threads(1)
y = (((k*k+3*k)-k/4)/k+k*k*k*k+k*k*(22/7*k)+k*k*k*k*k*k*k*k*k).sum()
start_time_pytorch = time.time()
y.backward()
k.grad

end_time_pytorch = time.time()
runtime = (end_time_pytorch - start_time_pytorch)
print(str(runtime))
k_list = k.grad.tolist()

for i in range(num_params):
	print(str(k_list[i]))
