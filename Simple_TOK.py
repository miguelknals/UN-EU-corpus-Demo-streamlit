"""
Usage:
    Simple_TOK.py --src=<file>
    
Options:
    -h --help       show this screen.
    --src=<file>    file to be tokenized
"""
import re
import time

import os
import subprocess
from docopt import docopt # http://docopt.org/
ja="@@"

class classMyClass(object):
    def __init__(self):
        self.value="Class value"
    
    def my_function(self, kk):
        # my funcition
        
        return self.value, kk
        

def my_function(kk):
    # my funcition
    return kk


def func_read_file(file):
    """ Read file and return list of lines.
    """
    with open(file, "r") as f:
        lines = f.readlines()
    return lines

class class_main_object(object):
    def __init__(self):
        self.value="Class value"
        self.TodoOk=True
    
    def my_function(self, kk):
        # my funcition
        
        return self.value, kk
    


def func_main_process(file_name):
    """ Main process.
    """
    file_name_tok=file_name+".tok"
    
        
    with open(file_name, encoding='utf-8', mode ='r') as ifile, \
        open(file_name_tok, encoding='utf-8', mode ='w' ) as ofile:

        nlin=0

        while True:
            printa()
            # print (vprinta, num_word_ofile1)
            nlin+=1    
            l1 = ifile.readline()
            if not l1:
                break  
            
            l2=f_tokenize(l1)
            todoOK= True
            if todoOK:
                ofile.write(l2 +"\n")

    return None



def detect_alphanumeric_word(text):
    pattern = re.compile(r'\b\w+\b')
    matches = pattern.findall(text)
    return matches
    

def f_tokenize(l1):
    """ Tokenize line.
    """
    list_num=[]
    num_num=0
    list_upper=[]
    word_l=l1.split()
    word_l2=[]
    for word in word_l:
        if word.isalpha(): # most simple case al alfa
            new_word=word
        else:
            # ned to analyze each char
            left_char=""
            right_char=""
            new_word=""
            for idx  in range(0, len(word)):
                # need to se left and right char
                if idx>=1:
                    left_char=word[idx-1]
                else:  # first char
                    left_char=""
                if idx<len(word)-1:
                    right_char=word[idx+1]
                else:  # last char                  
                    right_char=""
                #
                if word[idx].isalpha():
                    new_word+=word[idx]
                elif word[idx].isdigit():
                    if left_char!="":
                        new_word+=" " + ja + word[idx]
                    else:
                        new_word+= word[idx]
                    if right_char!="":
                        new_word+= ja+ " "
                    else:
                        new_word+= "" # ja 
                else: # not alfa or digit
                    if left_char!="":
                        new_word+=" " + ja + word[idx]
                    else:
                        new_word+= word[idx]
                    if right_char!="":
                        new_word+= ja+ " "
                    else:
                        new_word+= "" # ja 
            # split the text word in a list
        word_l=new_word.split(" ")
        for w in word_l:
            if w!="":
                bool_is_upper, uppertype = f_is_upper(w)
                if bool_is_upper:
                    word_l2.append(uppertype)
                    word_l2.append(w.lower())
                else:
                    word_l2.append(w)
                
    l1=" ".join(word_l2)
    return l1


def f_tokenize_old(l1):
    """ Tokenize line.
    """
    list_num=[]
    num_num=0
    list_upper=[]
    word_l=l1.split()
    new_word_l=[]
    for word in word_l:
        bool_is_upper, uppertype = f_is_upper(word)
        if bool_is_upper:
            new_word_l.append(uppertype)
            #new_word_l.append (word.lower())
        else:
            a=3
            #new_word_l.append(word.lower())
        # new_word is lower case
        # we need to check all chars
        word_lower=word.lower()
        if word_lower.isalpha(): # most simple case al alfa
            new_word_l.append(word_lower)
        else:
            # ned to analyze each char
            left_char=""
            right_char=""
            word=""
            for idx  in range(0, len(word_lower)):
                # need to se left and right char
                if idx>=1:
                    left_char=word_lower[idx-1]
                else:  # first char
                    left_char=""
                if idx<len(word_lower)-1:
                    right_char=word_lower[idx+1]
                else:  # last char                  
                    right_char=""
                #
                if word_lower[idx].isalpha():
                    word+=word_lower[idx]
                elif word_lower[idx].isdigit():
                    if left_char!="":
                        word+=" " + ja + word_lower[idx]
                    else:
                        word+= word_lower[idx]
                    if right_char!="":
                        word+= ja+ " "
                    else:
                        word+= "" # ja 
                else: # not alfa or digit
                    if left_char!="":
                        word+=" " + ja + word_lower[idx]
                    else:
                        word+= word_lower[idx]
                    if right_char!="":
                        word+= ja+ " "
                    else:
                        word+= "" # ja 
            # split the text word in a list
            word_l=word.split(" ")
            for w in word_l:
                if w!="":
                    new_word_l.append(w)

    l1=" ".join(new_word_l)
    return l1


def has_uppercase(string):
    return any(char.isupper() for char in string)

    
def f_is_upper(word):
    if len(word)==1:
        if word[0].isupper():                            
            bool_is_upper=True
            type="｟up｠"               
        else:
            bool_is_upper=False
            type=""                           
        return bool_is_upper, type

    # defalt values for upper cases or mixed cases for 2 words
    bool_is_upper=False
    type=""
    
    # at least 2 chars
    reminder=word[1:]
    reminder_has_uppercase=has_uppercase(reminder)
    # all lowercase
    if (word[0].islower() and reminder_has_uppercase==False): # first upper and reminder all lower
        bool_is_upper=False
        type=""
        return bool_is_upper, type
    # upper first, then lowercase
    if (word[0].isupper() and reminder_has_uppercase==False): # first upper and reminder all lower
        bool_is_upper=True
        type="｟up｠"
        return bool_is_upper, type
    # there are upper case in the reminder
    if (word[0].isupper() and reminder.isupper()): # first upper and reminder all upper
        bool_is_upper=True
        type="｟aup｠"
        return bool_is_upper, type
    # mixed case
    bool_is_upper=False
    type=""
    return bool_is_upper, type
    
    

def f_is_number (my_word):
    # this subrutine originally in sqlite_02_anaydewoards.py
    # 1234 123:23 12.322 or 12.2*2.2.2 are numbers
    bool_hasdigit=False
    bool_hasalfa=False
    bool_isnumber=False # by default not a number
    for c in my_word: # number unless alfa is found
        if (c.isalpha()):
            bool_hasalfa=True
            break
        if (not bool_hasdigit): # have not found a digit
            bool_hasdigit=c.isdigit() # let see is this it its            
    # we can arrive becasue if the brek
    if (not bool_hasalfa): # ok has no alfa
        if (bool_hasdigit): #but has digits is a number
            bool_isnumber=True

    return bool_isnumber


vprinta=0

def printa():
    # need to use vprinta = 0 at the start of main
    global vprinta
    vprinta+=1
    if (vprinta % 5000==0):
        print (".", end ="")  
    if (vprinta % 100000==0):
        print (" ", vprinta)




if __name__ == "__main__" :
    """ Main func.
    """    
    args = docopt(__doc__)
    
    FileSource=args["--src"]    
    
    vprinta=0  # as global variable
    
    start = time.process_time()
    func_main_process(FileSource)   
    print("t PRo = ", time.process_time() - start)    
        

    print ("End of test.")
     
    
    print("EOP.")
    
        
        
    
        
    