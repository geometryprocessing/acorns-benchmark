import torch
import time
import os

from subprocess import call

import forward_diff

print("Pytorch ---------------")
pytorchTimes = []
usTimes = []
for i in range(1):
	start_time_pytorch = time.time();

	x = torch.autograd.Variable(torch.Tensor([4]),requires_grad=True)
	y = torch.sin(x)*torch.cos(x)+torch.pow(x,2);
	y.backward()
	# print(x.grad)

	end_time_pytorch = time.time()

	runtime = end_time_pytorch - start_time_pytorch
	pytorchTimes.append(runtime)

averageRuntimePyTorch = sum(pytorchTimes) / len(pytorchTimes)
print("Runtime: " + str(averageRuntimePyTorch))

start_time_us = time.time()
forward_diff.main("file.c")
os.system("gcc c_code.c -o c_code -lm")

for i in range(1):
	call(["./c_code"])
	end_time_us = time.time()

	runtime = end_time_us - start_time_us
	usTimes.append(runtime)

averageRuntimeUs = sum(usTimes) / len(usTimes)
print("Runtime: " + str(averageRuntimeUs))
