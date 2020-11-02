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
_ = [os.remove(os.path.join('.','text',file)) for file in textfiles if 'part' in file.split('`')]
_ = [os.remove(os.path.join('.','text',file)) for file in textfiles if 'encrypt' in file.split('`')]
# Keep `.txt` files only
textfiles = [os.path.join('.','text',file) for file in textfiles
             if file.endswith('txt') and not 'encrypt' in file.split('`') and not 'part' in file.split('`')]
# Back up `class Caesar` with full text
CAESAR_init = {}
length_and_name = []
# Back up `Caesar` with different length
CAESAR = []

# Choose a random `offset`
OFFSET = np.random.randint(26)
# Maximum value for tolerance
TOLERANCE = 12

# Get text length
for text in textfiles:
    C = Caesar(offset=OFFSET)
    CAESAR_init[text] = {}
    CAESAR_init[text]['caesar'] = C
    C.read_file(text)
    CAESAR_init[text]['length'] = C.get_letter_count()
    length_and_name.append((CAESAR_init[text]['length'],text))

length_and_name = sorted(length_and_name, key=lambda x:x[0], reverse=True) # long => short

STEPS = int(np.log(length_and_name[0][0])/np.log(10))+1 # 10^2~n range(2,STEPS)=[2,STEPS)

# Accuracy(TOLERANCE,STEPS)
ACC = np.zeros((TOLERANCE,STEPS),dtype='float64')
# Accuracy of each text under each tolerance & length
acc = [0 for _ in range(len(textfiles))]

for step in range(2,STEPS):
    for tol in range(TOLERANCE):
        for itext, text in enumerate(textfiles):

            C = Caesar(offset=OFFSET,tolerance=tol)
            CAESAR.append(C)

            # read, encrypt and save file
            C.read_file(text)
            letter_count = C.get_letter_count()
            std_length = 10**step
            if std_length < letter_count:
                C.split_text(std_length/letter_count)
            else:
                continue
            #C.save_to_file(os.path.join('.','text','`part`'+' '+str(step).zfill(2)+'-'+str(STEPS)+text.split('`')[-1]))
            C.encrypt(text=C.splitted_text)
            #C.save_to_file(os.path.join('.','text','`encrypt`'+' '+str(step).zfill(2)+'-'+str(STEPS)+text.split('`')[-1]))

            # use letter frency method to decrypt text and calculate accuracy
            en_letter_frequency = C.get_letter_frequency()
            accuracy, offset = C.get_accuracy(en_letter_frequency,text=C.splitted_text)

            # save results
            acc[itext] = accuracy*100
        ACC[tol][step] = sum(acc)/len([i for i in acc if not i == 0])
        acc = [0 for _ in range(len(textfiles))]
        print('Loading...{:6.2f}%'.format(100*(TOLERANCE*step+tol)/(STEPS*TOLERANCE)))

# Plot result
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(1,1,1,projection='3d')
X = np.arange(STEPS)
Y = np.arange(TOLERANCE)
Z = ACC
X, Y = np.meshgrid(X, Y)
X, Y, Z = X.ravel(), Y.ravel(), Z.ravel()
height = np.zeros_like(Z)
width = 0.45
depth = 0.75
c = [[1-(z-min(Z))/(max(Z)-min(Z)), (z-min(Z))/(max(Z)-min(Z)), (z-min(Z))/(max(Z)-min(Z))/2] for z in Z]
ax.bar3d(X, Y, height, width, depth, Z, color=c)
ax.view_init(20, -125)
ax.set_title('Accuracy V.S. Length')
ax.set_xlabel('length/10^x')
ax.set_ylabel('tolerance')
ax.set_zlabel('accuracy/%')
#plt.show()
plt.savefig('Accuracy V.S. Length.jpg')
plt.close()
