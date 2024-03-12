# Code

### 1.Directory

```bash

│   AUTHORS                              作者信息
│   COPYING                              license信息
│   README                               简介和操作命令
│   TRAINING                             训练的操作命令
│   autogen.sh                           以下为编译相关部分
│   configure.ac                               
│   Makefile.am                               
│   update_version                          
│   rnnoise-uninstalled.pc.in                     
│   rnnoise.pc.in                              
│
├───doc
│       Doxyfile.in                      用于生成文档的配置
│
├───examples
│       rnnoise_demo.c                   使用库, 对输入的语音做降噪处理
│
├───include
│       rnnoise.h                        库函数接口
│
├───m4
│       attributes.m4                    宏，用于检查通用（非类型）符号的存在
│
├───src
│       compile.sh                       denoise_training的编译脚本
│       denoise.c                        库的相关接口函数, 以及denoise_training的main函数
│       rnn.c/h                          神经网络的计算函数, 包括GRU和全连接层(Dense)
│       rnn_data.c/h                     生成的权重数据, 以权重->层(layer)->模型的架构来组织
│       rnn_reader.c                     载入和释放模型数据的函数
│       celt_lpc.c/h                     CELT相关代码
│       kiss_fft.c/h, _kiss_fft_guts.h   kiss fft的相关代码
│       pitch.c/h                        基音(pitch)相关代码
│       tansig_table.h                   双曲正切S型函数的速查数据
│       arch.h, opus_types.h             架构和平台相关的定义和宏
│       common.h                         内存操作相关的宏/接
│       rnn_train.py                     另外一个版本的训练脚本
└───training
        bin2hdf5.py                      转换训练数据的格式: f32-> hdf5, 需要指定矩阵维度
        dump_rnn.py                      把权重转换为c代码, 到src\rnn_data.h|c
        rnn_train.py                     训练脚本, 包括构造模型, 载入和分配数据,训练,保存权重
```

空间滤波，说话滤波

旁边有人说话，

baseline,

realtime,

技术绿线，

频谱滤波，实时滤波，杨志雄，ppt

4.小分队
