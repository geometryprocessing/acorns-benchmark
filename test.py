import torch
import time

print("Pytorch ---------------")
pytorchTimes = []
for i in range(1000):
	start_time = time.time();

	x = torch.autograd.Variable(torch.Tensor([4]),requires_grad=True)
	y = torch.sin(x)*torch.cos(x)+torch.pow(x,2);
	y.backward()
	# print(x.grad)

	end_time = time.time()

	runtime = end_time - start_time
	pytorchTimes.append(runtime)

averageRuntime = sum(pytorchTimes) / len(pytorchTimes)
print("Runtime: " + str(averageRuntime))