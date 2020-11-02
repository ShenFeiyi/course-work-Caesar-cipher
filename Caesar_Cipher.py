# -*- coding:utf-8 -*-
import numpy as np
from matplotlib import pyplot as plt

class Caesar:
    def __init__(self, **kwarg):
        # Define the offset value of the encryption algorithm
        self.OFFSET = kwarg['offset'] if 'offset' in kwarg else 3
        # Standard letter frequency distribution table
        letter_frequency_reverse = 'zqxjkvbpygfwmucldrhsnioate' # low -> high
        self.LETTER_FREQUENCY_TABLE = [ letter for letter in letter_frequency_reverse ]
        self.LETTER_FREQUENCY_TABLE.reverse()
        # Define the number of types of letters in the text
        self.NUMBER_OF_LETTERS = len(self.LETTER_FREQUENCY_TABLE)
        # Original text
        self.text = ''
        # Splitted text
        self.splitted_text = ''
        # Encrypted text
        self.encrypted = ''
        # Tolerance
        self.tolerance = kwarg['tolerance'] if 'tolerance' in kwarg else 1
        '''
        tolerance (int, default=1):
            A hyperparameter to adjust the error tolerance. For example, if we use the letter frequency 
            decryption method and get the decrypted letter 'l', but the ground-truth is 'c', we can think 
            this is correct under the error tolerance 1, because the difference between the position of 'l' 
            and the position of 'c' in the LETTER_FREQUENCY_TABLE is only 1.
        '''

    def read_file(self, path):
        """Read file function
        Args:
            path (str): The path of the file to read.
        
        Returns:
            (None)
        """
        with open(path,'r',encoding='utf-8') as f:
            self.text = f.read()

    def split_text(self, fraction):
        """
        Args:
            fraction (float): `fraction` percent, (0,1)

        Returns:
            (None)
        """
        LENGTH = self.get_letter_count()
        length = int(fraction * LENGTH)
        try:
            start_point = np.random.randint(LENGTH-length)
        except ValueError:
            print(LENGTH,length)
        self.splitted_text = self.text[start_point:start_point+length]

    def encrypt(self, **kwarg):
        """Replacement encryption function

        Replace letters with the Caesar method: ASCII + OFFSET

        Args:
            kwarg (dict):
                text (str): The text content of the original file.
        
        Returns:
            (None)
        """
        text = kwarg['text'] if 'text' in kwarg else self.text
        encrypted_text = ''
        for c in text:
            if c >= 'A' and c <= 'Z':
                encrypted_text += chr(ord('A') + (ord(c)-ord('A') + self.OFFSET) % self.NUMBER_OF_LETTERS)
            elif c >= 'a' and c <= 'z':
                encrypted_text += chr(ord('a') + (ord(c)-ord('a') + self.OFFSET) % self.NUMBER_OF_LETTERS)
            else:
                encrypted_text += c
        self.encrypted = encrypted_text

    def save_to_file(self, path, **kwarg):
        """Save the result to a file

        Args:
            path (str): The path of the file to save.
            kwarg (dict):
                text (str): The text content of the file to save. Default = self.encrypt
        
        Returns:
            (None)
        """
        text = kwarg['text'] if 'text' in kwarg else self.encrypted
        with open(path,'w',encoding='utf-8') as f:
            f.write(text)

    def get_letter_count(self, **kwarg):
        """Count letters in the text

        Args:
            kwarg (dict):
                text (str): The text to count letters.
        
        Returns:
            letter_count (int): number of letters

        """
        text = kwarg['text'] if 'text' in kwarg else self.text
        letter_count = 0
        for c in text:
            if (c >= 'A' and c <= 'Z' ) or (c >= 'a' and c <= 'z'):
                letter_count += 1

        return letter_count

    def get_letter_frequency(self, **kwarg):
        """Letter frequency statistics on text
        
        Args:
            kwarg (dict):
                text (str): The text to calculate letter frequency.

        Returns:
            letter_frequency (dict): An unordered dictionary of the letter frequency, 
            i.e., {Key (char): letter, Value (float): frequency of the letter}
        """
        text = kwarg['text'] if 'text' in kwarg else self.encrypted
        letter_count = self.get_letter_count(text=text) # Get the total number of text letters
        letter_frequency = {} # Get the alphabet frequency dictionary

        for c in text:
            if (c >= 'A' and c <= 'Z' ) or (c >= 'a' and c <= 'z'):
                letter_frequency[c.lower()] = letter_frequency.get(c.lower(),0) + 1

        for key in letter_frequency:
            letter_frequency[key] /= letter_count
            
        return letter_frequency

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
        tol = self.tolerance
        origin_text = kwarg['text'] if 'text' in kwarg else self.text
        encrypted_text = self.encrypted
        letter_frequency = sorted(letter_frequency.items(), key=lambda x:x[1], reverse=True)
        frequency_table = [i[0] for i in letter_frequency]
        letter_count = self.get_letter_count(text=encrypted_text)

        guess_offset = {}
        count = 0
        for i, c in enumerate(encrypted_text):
            if (c >= 'A' and c <= 'Z' ) or (c >= 'a' and c <= 'z'):
                idx = frequency_table.index(c.lower())
                candidates = self.LETTER_FREQUENCY_TABLE[max(idx-tol, 0) : min(idx+tol+1, self.NUMBER_OF_LETTERS)]
                if (origin_text[i].lower() in candidates):
                    count += 1
                    offset_number = (ord(c.lower())-ord(self.LETTER_FREQUENCY_TABLE[idx].lower()))%self.NUMBER_OF_LETTERS
                    guess_offset[offset_number] = guess_offset.get(offset_number,0) + 1
        
        accuracy = count / letter_count
        try:
            offset_max = sorted(guess_offset.items(), key=lambda x:x[1], reverse=True)[0][0]
        except IndexError:
            offset_max = None
        return accuracy, offset_max

    def print_letter_frequency(self, letter_frequency, **kwarg):
        """Print the letter frequency

        Print the letter frequency with the format: "letter : frequency of the letter"

        Args:
            letter_frequency (dict): A dictionary of the letter frequency obtained by the `get_letter_frequency()` function.
            plot (bool): whether plot a diagram or not

        Returns:
            (None)
        """
        plot = kwarg['plot'] if 'plot' in kwarg else False
        letter_frequency = sorted(letter_frequency.items(), key=lambda x:x[1], reverse=True)
        for c, f in letter_frequency:
            print("%c : %.2f%%"%(c, 100*f),end='\t')

        if plot:
            fig = plt.figure()
            ax = fig.add_subplot(1,1,1)
            X = []
            Y = []
            for c, f in letter_frequency:
                X.append(c)
                Y.append(f)
            plt.bar(X, Y)
            ax.set_title('Letter Frequency')
            plt.show()

if __name__ == '__main__':
    C = Caesar(offset=3,tolerance=1)
    # read, encrypt and save file
    C.read_file('./text/`fiction` CHAPTER I A STRONG APPEAL.txt')
    C.encrypt()
    C.save_to_file('./text/`encrypt` CHAPTER I A STRONG APPEAL.txt')

    # use letter frency method to decrypt text and calculate accuracy
    letter_count = C.get_letter_count()
    en_letter_frequency = C.get_letter_frequency()
    accuracy, offset = C.get_accuracy(en_letter_frequency)

    # print results
    print("The letter frequency of the encrypted text:")
    C.print_letter_frequency(en_letter_frequency)
    print("The total number of letters in the origin text is %d."%(letter_count))
    print("The decryption accuracy is %.2f%% under tolerance %d."%(100*accuracy, C.tolerance))
    print(f"The most likely offset number is {offset}.")
