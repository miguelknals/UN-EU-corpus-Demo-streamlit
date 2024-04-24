"""
Usage:
    Simple_DETOK.py --src=<file>
    
Options:
    -h --help       show this screen.
    --src=<file>    file to be tokenized
"""
import re
import os
import subprocess
import time
vprinta=0
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
    

def tokenize(l):
    return l
    

def func_main_process(file_name):
    """ Main process.
    """
    file_name_detok=file_name+".detok"
    
        
    with open(file_name, encoding='utf-8', mode ='r') as ifile, \
        open(file_name_detok, encoding='utf-8', mode ='w' ) as ofile:

        nlin=0

        while True:
            printa()
            # print (vprinta, num_word_ofile1)
            nlin+=1    
            l1 = ifile.readline()
            if not l1:
                break  
            
            l2=f_detokenize(l1)
            todoOK= True
            if todoOK:
                ofile.write(l2 +"\n")

    return None



def f_detokenize(l1):
    """ Detokenize line.
    """
    
    lastw=""
    w_list=[]
    for w in l1.split():
        if w!="｟up｠" and w!="｟aup｠":
            if lastw=="｟up｠":
                new_w=w[0].upper()+w[1:]
            elif lastw=="｟aup｠":
                new_w=w.upper()
            else:
                new_w=w
            w_list.append(new_w)
        lastw=w
            
    l1=" ".join(w_list)
    l1=l1.replace(ja+" "+ja,"")
    l1=l1.replace(" "+ja,"")
    l1=l1.replace(ja+" ","")
    
    return l1
    
  
    
    
def f_is_upper(word):
    bool_is_upper=False
    type=""
    if (word[0].isupper() ): #or word[0].isdigit()):
        bool_is_upper=True
        type="｟aup｠"
        for c in word:
            if c.islower():
                type="｟up｠" # not all uupper
                break
        if len(word)==1:
            type="｟up｠" 
    
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
    
    
     
    
    print("EOP.")
    
        
        
    
        
    