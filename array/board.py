import os
import torch
import numpy as np
import torchaudio
import matplotlib.pyplot as plt

# 显示函数
def my_show(things, mode=True, pos=0, x=None, y=None):
    if mode:
        fig, axes = plt.subplots(len(things), 1)
        count = 0
        for item in things:
            if isinstance(item, np.ndarray):
                axes[count].plot(item[pos])
            else:
                axes[count].plot(np.array(item[pos]))
            axes[count].grid()
            count += 1
        plt.tight_layout()
    else:
        plt.plot(things)
        plt.grid()
    plt.xlabel(x)
    plt.ylabel(y)
    plt.show()

def my_read(file):
    waveform, sample_rate = torchaudio.load(file, normalize=False)
    waveform = waveform.float()
    waveform = waveform.mean(dim=0)
    return waveform, sample_rate

# 将一组音频信号打包，包括输入与输出
def group_things(make_root, out_root, group):
    show_range = range(group*2-1, group*2+1,1)
    print(show_range)
    things = []
    span = 150      # 由于周期性，只截取前一段处理
    # for i in show_range:
    #     file = make_root + "make{}.wav".format(i)
    #     waveform, sr = my_read(file)
    #     things.append((waveform[0:span], sr))
    for i in show_range:
        file = out_root + "div{}.wav".format(i)
        waveform, sr = my_read(file)
        things.append((waveform[0:span], sr))
    return things

def test_fft(input_signal):
    # 进行 FFT
    fft_result = np.fft.fft(input_signal)
    frequencies = np.fft.fftfreq(len(fft_result), d=1/16000)  # 计算频率

    # 找到主要频率成分的索引
    main_frequency_index = np.argmax(np.abs(fft_result))

    # 提取主要三角函数信号的频率和幅度
    main_frequency = abs(frequencies[main_frequency_index])
    main_amplitude = np.abs(fft_result[main_frequency_index]) / len(input_signal)

    print(f"主要频率成分：{main_frequency} Hz")
    print(f"主要频率成分的幅度：{main_amplitude}")

# 对组合中的每一项做fft变换
def my_fft(things, mode=True):
    res = []
    if mode:
        # 生成含有三角函数信号的示例数据
        t = np.linspace(0, 1, 16000, endpoint=False)
        f1 = 5  # 信号频率
        signal = np.sin(2 * np.pi * f1 * t)  # 生成正弦函数信号
        for item in things:
            test_fft(signal)
            fft = torch.fft.rfft(item[0], norm='forward')
            spectrum = torch.abs(fft)       # 得到幅度谱
            angle = torch.angle(fft)        # 得到相位谱
            freq_axis = torch.fft.fftfreq(len(spectrum), d=1/item[1])
            print(f"spectrum:{spectrum}")
            print(f"item[1]:{item[1]}")
            print(f"angle:{angle}")
            print(f"freq_axis:{freq_axis}")
            main_frequency_index = np.argmax(np.abs(fft))

            # 提取主要三角函数信号的频率和幅度
            main_frequency = abs(freq_axis[main_frequency_index])
            print(f"main_frequency:{main_frequency}")
            res.append((spectrum, angle))
    return res

if __name__ == '__main__':
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
    group = 1

    make_root = 'D:/7.intelligent/data/4.Audio/data/artificial/'
    out_root = 'D:/7.intelligent/data/4.Audio/data/out/'
    things = group_things(make_root, out_root, group)
    my_show(things)

    ffts = my_fft(things)
    my_show(ffts, pos=0)    # 显示幅度谱
