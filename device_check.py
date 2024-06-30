import torch

# 检查GPU设备
if torch.cuda.is_available():
    print(f"GPU 设备数量: {torch.cuda.device_count()}")
    for i in range(torch.cuda.device_count()):
        print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
else:
    print("没有GPU设备可用")

# CPU信息，默认情况下PyTorch总是支持CPU
print("CPU 设备:")
print(torch.device('cpu'))