import wave
import os
import numpy as np

dir_name = os.path.dirname(os.path.realpath(__file__))

rate = 16000  # 采样率
duration = 3  # 持续时间（秒）
frequency = 1  # 频率（Hz）

# 生成音频信号
t = np.linspace(0, duration, int(rate * duration))
audio_signal = np.sin(2 * np.pi * frequency * t)

# 标准化音频信号
audio_signal *= 32767 / np.max(np.abs(audio_signal))

# 创建WAV文件
with wave.open(dir_name+'/audios/output.wav', 'w') as sound_file:
    sound_file.setnchannels(1)  # 单声道
    sound_file.setsampwidth(2)  # 16位
    sound_file.setframerate(rate)  # 设置采样率
    sound_file.writeframes(audio_signal.astype(np.int16).tobytes())