import torch
import time
import numpy as np
import torch.autograd.functional as F

num_vars = 1
num_params = 10
T = torch.tensor(np.load('./tests/utils/numpy_params/function_0_param_T.npy'), requires_grad=True, dtype=torch.float)
torch.set_num_threads(1)

def make_func(T):
     return (4*((T * (1 - T)))).sum()
     
start_time_pytorch = time.time()

hessians = F.hessian(make_func, (T.data))

end_time_pytorch = time.time()
runtime = (end_time_pytorch - start_time_pytorch)
print(str(runtime))

data = []
if num_vars > 1:
     for j, hessian in enumerate(hessians):
          for k, tup in enumerate(hessian):
               tup_data = tup.data.numpy()
               tup_list = []
               for i in range(num_params):
                    tup_list.append(tup_data[i][i])
               data.append(tup_list)
else:
     tup_list = []
     for j, hessian in enumerate(hessians):
          hess_data = hessian.data.numpy()
          tup_list.append(hess_data[j])
     data.append(tup_list)
 
for i in range(num_params):
     for j in range(len(data)):
          print(data[j][i])