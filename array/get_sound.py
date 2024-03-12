import pyaudio
import wave
import os 
import numpy as np

p = pyaudio.PyAudio()

info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

def get_idx():
    for i in range(0, numdevices):
            if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
                if p.get_device_info_by_host_api_device_index(0, i).get('name').find("Array")!=-1:
                     return i
RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 6 # change base on firmwares, default_firmware.bin as 1 or i6_firmware.bin as 6
RESPEAKER_WIDTH = 2
# run getDeviceInfo.py to get index
RESPEAKER_INDEX = get_idx()  # refer to input device id
CHUNK = 1024
RECORD_SECONDS = 5  # s
dir_name = os.path.dirname(os.path.realpath(__file__))

   
stream = p.open(
            rate=RESPEAKER_RATE,
            format=p.get_format_from_width(RESPEAKER_WIDTH),
            channels=RESPEAKER_CHANNELS,
            input=True,
            input_device_index=RESPEAKER_INDEX,)

print("* recording")

frames = [[] for i in range(6)]# 创建一个空列表，用于存储录制的音频数据

for i in range(0, int(RESPEAKER_RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)  # 从音频流中读取指定长度的数据块
    all_channels_data = np.frombuffer(data, dtype=np.int16)  # 将所有6个通道的数据读取到数组中
    for channel in range(6):
        channel_data = all_channels_data[channel::6]  # 提取指定通道的数据
        frames[channel].append(channel_data.tobytes())  # 将提取的数据转换为字节并添加到 frames 列表中


print("* done recording")

stream.stop_stream()  # 停止音频流
stream.close()  # 关闭音频流
p.terminate()  # 终止 PyAudio 对象

for i in range(6):
    name = dir_name+"/audios/o_put"+str(i)+".raw"
    wf = wave.open(name, 'wb')  # 打开一个 RAW 文件用于写入音频数据，'wb' 表示二进制写入模式
    wf.setnchannels(1)  # 设置声道数为 1
    wf.setsampwidth(p.get_sample_size(p.get_format_from_width(RESPEAKER_WIDTH)))  # 设置每个采样点的位数
    wf.setframerate(RESPEAKER_RATE)  # 设置采样率
    wf.writeframes(b''.join(frames[i]))  # 将 frames 列表中的音频数据合并为一个字节串并将其写入到 RAW 文件中
    wf.close()  # 关闭 WAV 文件
