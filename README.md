

# Caesar Cipher

[TOC]



## 0. Questions & Answers

### Questions

Using a statistical method to unencrypt a Caesarean-encrypted text and analysing correlated parameters, including

1. tolerance
2. text length
3. different types of the article
4. different themes of the same type of article

### Answers

**Basic idea**: 

Calculate the frequency of each letter in the encrypted text and compare the frequency with the standard one. 

**Corresponding answers**: 

1. Using different tolerances and plot the answer. 
2. Cut the original text into different lengths and compare the average accuracy of each length. 
3. Compare the average accuracy of each type. 
4. Compare the average accuracy of each theme. 



## 1. Requirements 

- Python 3.7.3
- numpy 1.18.5
- matplotlib 3.3.2
- beautifulsoup4 4.9.3



## 2. Codes

### search_texts.py

search texts online

```python
# -*- coding:utf-8 -*-
import os
import re
import time
import requests
from bs4 import BeautifulSoup as BS

START = time.time()

base_url = 'https://www.cgtn.com/'
category = ['Business','Politics','Opinions','Culture','Sports','Travel','Nature']

save_path = 'text'

base_response = requests.get(base_url)
base_soup = BS(base_response.text,'html.parser')
for cate in category:
    with open(os.path.join('.',save_path,'`news` `'+cate.lower()+'` CGTN.txt'),'w') as file:
        base_result = base_soup.find_all('li',{'data-click-name':cate})
        for base_res in base_result:
            if not base_res is None:
                base_http = re.search('http',str(base_res))
                base_cate = re.search(cate.lower(),str(base_res))
                cate_url = str(base_res)[base_http.span()[0]:base_cate.span()[1]]
                cate_response = requests.get(cate_url)
                cate_soup = BS(cate_response.text,'html.parser')
                cate_result = cate_soup.find_all('h4')
                for cate_res in cate_result:
                    if not cate_res is None:
                        cate_http = re.search('http',str(cate_res))
                        cate_html = re.search('html',str(cate_res))
                        if (not cate_http is None) and (not cate_html is None):
                            news_url = str(cate_res)[cate_http.span()[0]:cate_html.span()[1]]
                            news_response = requests.get(news_url)
                            news_soup = BS(news_response.text,'html.parser')
                            news_result = news_soup.find_all('p')
                            for news_res in news_result:
                                news_head = re.search('<p>',str(news_res))
                                news_end = re.search('</p>',str(news_res))
                                if (not news_head is None) and (not news_end is None):
                                    news_almost = str(news_res)[news_head.span()[1]:news_end.span()[0]]
                                    inside = False
                                    for c in news_almost:
                                        if c == '<':
                                            inside = True
                                        if not inside:
                                            file.write(c)
                                        if c == '>':
                                            inside = False
                FINISH = time.time()
                print('{:.2f} seconds.'.format(FINISH-START))

FINISH = time.time()
print('Using {:.2f} seconds.'.format(FINISH-START))
```

### Caesar_Cipher.py

```python
# Define class Caesar here
class Caesar:
    def __init__(self, **kwarg):
        # Define the offset value of the encryption algorithm
        self.OFFSET = kwarg['offset'] if 'offset' in kwarg else 3
        # Original text
        self.text = ''
        # Splitted text
        self.splitted_text = ''
        # Encrypted text
        self.encrypted = ''
        # Tolerance
        self.tolerance = kwarg['tolerance'] if 'tolerance' in kwarg else 1
        # ...
```

#### Methods in `class Caesar`

1. Read file

    Read the given file and save it to `self.text`

    ```python
    def read_file(self, path):
        """Read file function
        Args:
            path (str): The path of the file to read.
    
        Returns:
            (None)
        """
        # ...
        # self.text = ...
    ```

2. Split file

    Split `self.text` into the given length and save it to `self.splitted_text`

    ```python
    def split_text(self, fraction):
        """Split text function, for different text length
        Args:
            fraction (float): `fraction` percent, (0,1)
    
        Returns:
            (None)
        """
        # ...
        # self.splitted_text = ...
    ```

3. Encrypt file

    Encrypt the original file, could be `self.text` or `self.splitted_text`

    ```python
    def encrypt(self, **kwarg):
        """Replacement encryption function
    
        Replace letters with the Caesar method: ASCII + OFFSET
    
        Args:
            kwarg (dict):
                text (str): The text content of the original file.
    
        Returns:
            (None)
        """
        # ...
        # self.encrypted = ...
    ```

4. Save file

    ```python
    def save_to_file(self, path, **kwarg):
        """Save the result to a file
    
        Args:
            path (str): The path of the file to save.
            kwarg (dict):
                text (str): The text content of the file to save. Default = self.encrypt
    
        Returns:
            (None)
        """
        # ...
    ```

5. Count the total letter in the text

    ```python
    def get_letter_count(self, **kwarg):
        """Count letters in the text
    
        Args:
            kwarg (dict):
                text (str): The text to count letters.
    
        Returns:
            letter_count (int): number of letters
    
        """
        # ...
        return letter_count
    ```

6. Calculate the frequency of each letter

    ```python
    def get_letter_frequency(self, **kwarg):
        """Letter frequency statistics on text
    
        Args:
            kwarg (dict):
                text (str): The text to calculate letter frequency.
    
        Returns:
            letter_frequency (dict): An unordered dictionary of the letter frequency, 
            i.e., {Key (char): letter, Value (float): frequency of the letter}
        """
        # ...
        return letter_frequency
    ```

7. Calculate the accuracy

    ```python
    def get_accuracy(self, letter_frequency, **kwarg):
        """Calculate the decryption accuracy of the letter frequency method
    
        Args:
            letter_frequency (dict): A dictionary of the letter frequency obtained by the `get_letter_frequency()` function.
            origin_text (str): unencrypted text, kwarg['text']
    
        Returns:
            accuracy (float): The decryption accuracy of the letter frequency method, i.e., the number of correctly decrypted 
                            letters / the total number of letters.
            guess_offset (dict):
        """
        # ...
        return accuracy, offset_max
    ```

8. Print/show result

    ```python
    def print_letter_frequency(self, letter_frequency, **kwarg):
        """Print the letter frequency
    
        Print the letter frequency with the format: "letter : frequency of the letter"
    
        Args:
            letter_frequency (dict): A dictionary of the letter frequency obtained by the `get_letter_frequency()` function.
            plot (bool): whether plot a diagram or not
    
        Returns:
            (None)
        """
        # ...
    ```

### main-tolerance.py

Plot the relationships between *accuracy* and *tolerance*

```python
# -*- coding:utf-8 -*-
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
```

### main-length.py

Plot the relationships between *accuracy*, *tolerance* and *article length*

```python
# -*- coding:utf-8 -*-
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
plt.savefig('Accuracy V.S. Length.jpg')
plt.close()
```

### main-types.py

Plot the relationships between *accuracy*, *tolerance* and *article types*

```python
# -*- coding:utf-8 -*-
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
# Classify files
filetypes = {}
types = [file.split('`')[1] for file in textfiles]
for t in types:
    if not t in filetypes:
        filetypes[t] = [file for file in textfiles if t in file.split('`')]

# Back up `Caesar`
CAESAR = []

# Choose a random `offset`
OFFSET = np.random.randint(26)
# Maximum value for tolerance
TOLERANCE = 12

# Accuracy(TOLERANCE,len(filetypes))
ACC = np.zeros((TOLERANCE,len(filetypes)),dtype='float64')
# Accuracy of each type of text under each tolerance
acc = [0 for _ in range(len(textfiles))]

for tol in range(TOLERANCE):
    for itypes, types in enumerate(filetypes):
        for itext, text in enumerate(filetypes[types]):

            C = Caesar(offset=OFFSET,tolerance=tol)
            CAESAR.append(C)

            # read, encrypt and save file
            C.read_file(text)
            C.encrypt()
            #C.save_to_file(os.path.join('.','text','`encrypt`'+' '+str(step).zfill(2)+'-'+str(STEPS)+text.split('`')[-1]))

            # use letter frency method to decrypt text and calculate accuracy
            letter_count = C.get_letter_count()
            en_letter_frequency = C.get_letter_frequency()
            accuracy, offset = C.get_accuracy(en_letter_frequency)

            # save results
            acc[itext] = accuracy*100
        ACC[tol][itypes] = sum(acc)/len([a for a in acc if not a == 0])
        acc = [0 for _ in range(len(textfiles))]
        print('Loading...{:6.2f}%'.format(100*(tol*len(filetypes)+itypes)/(len(filetypes)*TOLERANCE)))

# Plot result
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(1,1,1,projection='3d')
X = np.arange(len(filetypes))
Y = np.arange(TOLERANCE)
Z = ACC
plt.xticks(range(len([item for item in filetypes])), [item for item in filetypes])
X, Y = np.meshgrid(X, Y)
X, Y, Z = X.ravel(), Y.ravel(), Z.ravel()
height = np.zeros_like(Z)
width = 0.3
depth = 0.8
c = [[1-(z-min(Z))/(max(Z)-min(Z)), (z-min(Z))/(max(Z)-min(Z)), (z-min(Z))/(max(Z)-min(Z))/2] for z in Z]
ax.bar3d(X, Y, height, width, depth, Z, color=c)
ax.view_init(21, -125)
ax.set_title('Accuracy V.S. Types')
ax.set_xlabel('types')
ax.set_ylabel('tolerance')
ax.set_zlabel('accuracy/%')
plt.savefig('Accuracy V.S. Types.jpg')
plt.close()
```

### Main-themes.py

Plot the relationships between *accuracy*, *tolerance* and *article themes*

```python
# -*- coding:utf-8 -*-
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
# Classify files, choose `news` for example
textfiles = [file for file in textfiles if 'news' in file.split('`')]
themes = [file.split('`')[3] for file in textfiles]
filethemes = {}
for theme in themes:
    if not theme in filethemes:
        filethemes[theme] = [file for file in textfiles if theme in file.split('`')]

# Back up `Caesar`
CAESAR = []

# Choose a random `offset`
OFFSET = np.random.randint(26)
# Maximum value for tolerance
TOLERANCE = 12

# Accuracy(TOLERANCE,len(filethemes))
ACC = np.zeros((TOLERANCE,len(filethemes)),dtype='float64')
# Accuracy of each theme of text under each tolerance
acc = [0 for _ in range(len(textfiles))]

for tol in range(TOLERANCE):
    for itheme, theme in enumerate(filethemes):
        for itext, text in enumerate(filethemes[theme]):

            C = Caesar(offset=OFFSET,tolerance=tol)
            CAESAR.append(C)

            # read, encrypt and save file
            C.read_file(text)
            C.encrypt()
            #C.save_to_file(os.path.join('.','text','`encrypt`'+' '+str(step).zfill(2)+'-'+str(STEPS)+text.split('`')[-1]))

            # use letter frency method to decrypt text and calculate accuracy
            letter_count = C.get_letter_count()
            en_letter_frequency = C.get_letter_frequency()
            accuracy, offset = C.get_accuracy(en_letter_frequency)

            # save results
            acc[itext] = accuracy*100
        ACC[tol][itheme] = sum(acc)/len([a for a in acc if not a == 0])
        acc = [0 for _ in range(len(textfiles))]
        print('Loading...{:6.2f}%'.format(100*(tol*len(filethemes)+itheme)/(len(filethemes)*TOLERANCE)))

# Plot result
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(1,1,1,projection='3d')
X = np.arange(len(filethemes))
Y = np.arange(TOLERANCE)
Z = ACC
plt.xticks(range(len([item for item in filethemes])), [item for item in filethemes], rotation=-60)
X, Y = np.meshgrid(X, Y)
X, Y, Z = X.ravel(), Y.ravel(), Z.ravel()
height = np.zeros_like(Z)
width = 0.3
depth = 0.8
c = [[1-(z-min(Z))/(max(Z)-min(Z)), (z-min(Z))/(max(Z)-min(Z)), (z-min(Z))/(max(Z)-min(Z))/2] for z in Z]
ax.bar3d(X, Y, height, width, depth, Z, color=c)
ax.view_init(18, -115)
ax.set_title('Accuracy V.S. Themes')
ax.set_ylabel('tolerance')
ax.set_zlabel('accuracy/%')
plt.savefig('Accuracy V.S. Themes.jpg')
plt.close()
```



## 3. Result

### 3.1. Tolerance

<img src='Accuracy V.S. Tolerance.jpg' style='zoom:75%'>

### 3.2. Length

<img src='Accuracy V.S. Length.jpg'>

### 3.3. Types

<img src='Accuracy V.S. Types.jpg'>

### 3.4. Themes

<img src='Accuracy V.S. Themes.jpg'>

