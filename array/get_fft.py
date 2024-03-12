import os
import numpy as np
import matplotlib.pyplot as plt

dir_name = os.path.dirname(os.path.realpath(__file__))
file_path  = [dir_name+"/audios/o_put"+str(i)+".raw" for i in range(1,5)]
# file_path  = dir_name+"/audios/output.wav"

speed_of_speech = 343   # m/s
d = 0.032  # m
t_max = d*2/speed_of_speech*1000    # ms
def plt_show(frequencies,fft_result):
    plt.figure(figsize=(12, 6))
    idx = 0
    for fre,res in zip(frequencies,fft_result):
        idx+=1
        # 绘制频谱图
        plt.subplot(4, 1, idx)
        plt.plot(fre, np.abs(res))
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Amplitude')
        plt.title(f'FFT Spectrum {idx}')


    plt.tight_layout()
    plt.show()


def fft_fk(files):
    fre_list = []
    fft_list = []
    print(f"files:{files}")
    for idx,file_path in enumerate(files):
        with open(file_path, 'rb') as f:
            raw_data = np.fromfile(f, dtype=np.int16)  # 假设数据是16位有符号整数
        
        # 进行 FFT
        fft_result = np.fft.fft(raw_data)
        frequencies = np.fft.fftfreq(len(fft_result), d=1/16000)  # 计算频率
        fft_list.append(fft_result)
        fre_list.append(frequencies)
        # 找到主要频率成分的索引
        main_frequency_index = np.argmax(np.abs(fft_result))

        # 提取主要三角函数信号的频率和幅度
        main_frequency = abs(frequencies[main_frequency_index])
        main_amplitude = np.abs(fft_result[main_frequency_index]) / len(raw_data)
        print(f"{idx+1}号麦克风:")
        print(f"主要频率成分：{main_frequency} Hz")
        print(f"主要频率成分的幅度：{main_amplitude}")
    return fre_list,fft_list

def fft(files):
    channel = [{} for i in range(len(files))]
    index = []
    for idx,file in enumerate(files):
        channel[idx]['fre'] = []
        channel[idx]['phase'] = []
        channel[idx]['amplitude'] = []
        with open(file, 'rb') as f:
            raw_data = np.fromfile(f, dtype=np.int16)  # 假设数据是16位有符号整数
        # 进行 FFT
        fft_result = np.fft.fft(raw_data)
        frequencies = np.fft.fftfreq(len(fft_result), d=1/16000)  # 计算频率
        phase = np.angle(fft_result,deg=True)   # 计算相位
        # 找到主要频率成分的索引
        main_frequency_index = np.argsort(np.abs(fft_result))[-10:][::-1]
        # 获取主要频率对应的频率和相位
        main_frequencies = abs(frequencies[main_frequency_index])
        main_amplitude = abs(fft_result[main_frequency_index]) / len(raw_data)
        main_phase = abs(phase[main_frequency_index])
        channel[idx]['fre'].append(main_frequencies)
        channel[idx]['phase'].append(main_phase)
        channel[idx]['amplitude'].append(main_amplitude)
        index.append(main_amplitude[0])
    index = np.argsort(index)
    max_index = get_idx(index)
    return channel,max_index

def get_idx(index):
    """获取8个区域范围"""
    if index[-1]==0:
        if index[-2]==1:
            return 1
        else:
            return 8
    elif index[-1]==1:
        if index[-2]==0:
            return 2
        else:
            return 3
    elif index[-1]==2:
        if index[-2]==1:
            return 4
        else:
            return 5
    elif index[-1]==3:
        if index[-2]==0:
            return 7
        else:
            return 6

def signal_align(files):
    """时域信号对齐
        1.采样率 16000
        2.根据4通道的幅值判断对齐对象,所在象限
        3.找到时间差
        4.根据时间差判断位置
        5.人说话的频率范围通常在大约 85 Hz 到 255 """
    step_t = 1/16   # 采样时间片
    channels,index = fft(files)
    print(index)
    print(channels)
    for channel in channels:
        t = [(np.pi/2-p)/2*1000/np.pi/f for f,p in zip(channel['fre'],channel['phase'])]
        print(t)

if __name__=="__main__":
    fre,res = fft_fk(file_path)
    signal_align(file_path)
    plt_show(fre,res)