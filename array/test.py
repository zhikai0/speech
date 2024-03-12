import numpy as np
import matplotlib.pyplot as plt

# 生成含有三角函数信号的示例数据
t = np.linspace(0, 1, 1000, endpoint=False)
f1 = 5  # 信号频率
signal = np.sin(2 * np.pi * f1 * t)  # 生成正弦函数信号
noise = 0.5 * np.random.normal(size=t.size)  # 加入噪声
input_signal = signal + noise  # 合成含噪声的信号

# 进行 FFT
fft_result = np.fft.fft(input_signal)
frequencies = np.fft.fftfreq(len(fft_result), d=1/1000)  # 计算频率

# 找到主要频率成分的索引
main_frequency_index = np.argmax(np.abs(fft_result))

# 提取主要三角函数信号的频率和幅度
main_frequency = abs(frequencies[main_frequency_index])
main_amplitude = np.abs(fft_result[main_frequency_index]) / len(input_signal)

print(f"主要频率成分：{main_frequency} Hz")
print(f"主要频率成分的幅度：{main_amplitude}")