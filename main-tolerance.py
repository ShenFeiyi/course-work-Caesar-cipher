# -*- coding:utf-8 -*-
'''
本题提供文本加密、字母频率统计以及频率分析法破解精度计算的Python3程序，请使用该程序进行以下分析：

(1)分析不同错误容忍度（程序中tolerance超参数）对破解精度的影响。

(2)分析不同的加密文本长度对破解精度的影响

(3)分析不同类型的文本（学术、小说、新闻…）对破解精度的影响

(4)分析同一类型中不同主题的文本（如新闻文本包含科技、政治、体育等不同主题）对破解精度的影响。

需要提交：

（1）程序文档，文档结构包括：问题描述、主要算法或者模型、实验数据及分析、有关说明（如引用他人程序说明）；

（2）程序源代码，其中需要包含注释，以及程序运行环境的说明；

（3）提交方式：将有关文件打包成 xxP1.zip, 其中xx为学号，并上传到pintia.cn中。
'''
import os
import numpy as np
from matplotlib import pyplot as plt

from Caesar_Cipher import Caesar

# Read files
textfiles = os.listdir(os.path.join('.','text'))
# Delete saved files, if any
_ = [os.remove(os.path.join('.','text',file)) for file in textfiles if 'encrypt' in file.split('`')]
# Keep `.txt` files only
textfiles = [os.path.join('.','text',file) for file in textfiles if file.endswith('txt') and not 'encrypt' in file.split('`')]
# Back up every `class Caesar`
CAESAR = []

# Choose a random `offset`
OFFSET = np.random.randint(26)
# Maximum value for tolerance
TOLERANCE = 25
# Accuracy under every tolerance, initialize
ACC = np.zeros(TOLERANCE,dtype='float64')
# Accuracy under a specific tolerance, initialize
acc = [-1 for _ in range(len(textfiles))]

for tol in range(TOLERANCE):
    for itext, text in enumerate(textfiles):

        C = Caesar(offset=OFFSET,tolerance=tol)
        CAESAR.append(C)

        # read, encrypt and save file
        C.read_file(text)
        C.encrypt()
        #C.save_to_file(os.path.join('.','text','`encrypt`'+text.split('`')[-1]))

        # use letter frency method to decrypt text and calculate accuracy
        letter_count = C.get_letter_count()
        en_letter_frequency = C.get_letter_frequency()
        accuracy, offset = C.get_accuracy(en_letter_frequency)

        # save results
        acc[itext] = accuracy*100
    ACC[tol] = sum(acc)/len(acc)
    acc = [-1 for _ in range(len(textfiles))]
    print('Loading...{:6.2f}%'.format(100*(tol+1)/TOLERANCE))

# Plot result
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(1,1,1)
X = np.arange(TOLERANCE)
Y = ACC
c = [[1-(a-min(ACC))/(max(ACC)-min(ACC)), (a-min(ACC))/(max(ACC)-min(ACC)), (a-min(ACC))/(max(ACC)-min(ACC))/2] for a in ACC]
plt.bar(X,Y,color=c)
plt.plot(np.array([0,24]),np.array([60,60]),'b*-')
plt.plot(np.array([0,24]),np.array([100,100]),'r*-')
ax.set_title('Accuracy V.S. Tolerance')
ax.set_xlabel('tolerance')
ax.set_ylabel('accuracy/%')
plt.savefig('Accuracy V.S. Tolerance.jpg')
plt.close()
