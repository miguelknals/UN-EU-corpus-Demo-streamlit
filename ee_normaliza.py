
"""
Usage:
    ee_normaliza toklist   --corpus=<file>  --tokfile=<file> 
    ee_normaliza tokenize  --src=<file> [ --tgt=<file> ] --tokfile=<file> [ --tagcasing=<boolean> ] [ --varnum=<boolean> ]
    ee_normaliza detokenize  --src=<file> --varfile=<file>
    
Options:
    -h --help                               show this screen.
    --src=<file>                            src file
    --tgt=<file>                            tgt file
    --corpus=<file>                         corpus file (use with toklist command)
    --tokfile=<file>                        symbol list file for tokenize
    --varfile=<file>                         variable file for detokenization
    --tagcasing=<boolean>                   tag casing True or false [default: True].
    --varnum=<boolean>                      variable creation True or false [default: True].
"""


from docopt import docopt


#from posix import times_result
#from ja_uppercase import func_is_upper
import os 
import sys
# sys
#auxS = os.path.join("..","00_mono")
#sys.path.insert(1, auxS)
#auxS="/u_Mlai32/21_T4T/02_py/00_mono"
#sys.path.insert(1, auxS)

from bc_normalizer_V03 import normalize_tokenize_file, normalize_detokenize_file


global vprinta
vprinta=0


def  variable_replenishment(if1, of1, ivariablelistfile):
    s_ifile1=if1
    s_ofile1=of1
    s_varfile=ivariablelistfile

    with open(s_ifile1, encoding='utf-8', mode ='r') as ifile1, \
        open(s_ofile1, encoding='utf-8', mode ='w' ) as ofile1, \
        open(s_varfile, encoding='utf-8', mode ='r' ) as ivarfile:

        while True:
            
            printa()
            # print (vprinta, num_word_ofile1)
            if vprinta ==  1000E6:
                break
            #print (vprinta) 
            if vprinta==100:
                print("")
            l1 = ifile1.readline()
            l2= ivarfile.readline()
            l1= l1.rstrip("\n")
            l2= l2.rstrip("\n")
            if not l1:
                break 
            l1= f_var_repl_line(l1,l2)
            ofile1.write(l1+ "\n")


def f_var_repl_line (l1,l2):
    new_word_l=[]
    word_l=l1.split() # list of 
    var_l=l2.split() # list of variable
    ele_l=len(word_l)
    idx=0
    idx_var=0 #varible list index
    while idx < ele_l: #something to do
        w=word_l[idx] #
        nw=word_l[idx] # by default new word is same as previous
        if w.find("｟aup｠")>=0: # it can be with nother cahar ("")
            nw=w.replace("｟aup｠","")
            if len (word_l)  > idx+1 :
                idx+=1               
                nw=nw+ word_l[idx].upper()
        elif w.find("｟up｠")>=0:
            nw=w.replace("｟up｠","")
            if len (word_l) > idx +1:  
                idx+=1               
                auxs=word_l[idx]
                nw+= auxs[0].upper() + auxs[1:]
            
        elif len(w) > 3:
            r1=w.find("｟n")
            if r1 >=0:
                r2=w.find("｠",r1)
                if r2 >=0:
                    if len(var_l) -1 >= idx_var:
                        nw=w[0:r1]+ var_l[idx_var] +w[r2+1:]
                        idx_var+=1
                    else:                        
                        nw=w[0:r1]+ w +w[r2+1:] # leave w
                        #nw=w[0:r1]+ "" +w[r2+1:] # or remove
            
        if nw !="":
            new_word_l.append(nw)
        idx+=1    
    return ' '.join(new_word_l)
    



def variable_replacement (if1,of1,tagcasing,varnum):
    s_ifile1= if1
    s_ofile1=of1
    with open(s_ifile1, encoding='utf-8', mode ='r') as ifile1, \
        open(s_ofile1, encoding='utf-8', mode ='w' ) as ofile1, \
        open(s_ofile1+".var", encoding='utf-8', mode ='w' ) as ofile2: 
        #open(s_ofile1+".debug", encoding='utf-8', mode ='w' ) as ofile3:
        
        #boolDebuga=True

        while True:
            printa()
            # print (vprinta, num_word_ofile1)
            if vprinta == 1000000000:
                break

            if vprinta == 960:
                print ("")

            l1 = ifile1.readline()
            if not l1:
                break             

            l1=l1.rstrip("\n")
            l1, listnum = fc_replace_variable(l1,tagcasing,varnum) # tagcasing True replace 
            ofile1.write (l1+"\n")
            lvar=""
            for var in listnum:
                lvar+=var+ " "
            ofile2.write(lvar+"\n")
            
    ifile1.close()
    ofile1.close()


def fc_replace_variable(l1,tagcasing,varnum):
    list_num=[]
    num_num=0
    list_upper=[]
    word_l=l1.split()
    new_word_l=[]
    for word in word_l:
        if f_is_number(word) and varnum==True:
            list_num.append(word)
            new_word_l.append( "｟n" + str(num_num) +"｠")
            num_num+=1
        else:
            if tagcasing:
                bool_is_upper, uppertype = f_is_upper(word)
                if bool_is_upper:
                    new_word_l.append(uppertype)
                    new_word_l.append (word.lower())
                else:
                    new_word_l.append(word.lower())
            else: # no casing
                new_word_l.append(word) # no casing

    l1=" ".join(new_word_l)
    return l1, list_num


def fc_replace_variable_old(l1):
    list_num=[]
    list_upper=[]
    word_l=l1.split()
    sentencepos=0
    for word in word_l:
        if f_is_number(word):
            list_num.append(word)
            s="ÇÇÇÇÇ"
            l1=l1.replace(word,s,1)
        else:
            bool_is_upper, uppertype = f_is_upper(word)
            if bool_is_upper:
                list_upper.append([word, uppertype])
                s="ÑÑÑÑÑ"
                l1=l1.replace(word,s,1)

    # number replacemnt
    idx=0
    for n in list_num:
        s="｟n" + str(idx) +"｠"
        l1= l1.replace("ÇÇÇÇÇ",s,1)
        idx+=1
    idx=0
    for n in list_upper:
        word=n[0]
        type=n[1]
        s="｟"+ type + "｠"
        l1= l1.replace("ÑÑÑÑÑ",s + " "+ word,1)
        idx+=1
    
    l1=l1.lower()

    return l1, list_num



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

def f_main_tokeniza(myFileList,tagcasing,tokenlist,varnum):
    for myFile in myFileList:        
        ifile= myFile
        ofiletmp =ifile + ".tmp"
        ofile1=  ifile + ".tok.tc"
        print ("Tokenizing the file...")
        print (myFile)
        normalize_tokenize_file(ifile,ofiletmp, tokenlist )
        # numbers to NN
        print ("Starting variable replacement...")
        variable_replacement(ofiletmp,ofile1,tagcasing,varnum)


def f_main_detokeniza(myFileList):
    for myFile, myFileVar in myFileList:        
        ifile= myFile
        ofiletmp=ifile + ".tmp"
        ofile1=  ifile + ".dtok.4cl"
        ofilevariablelist=myFileVar
        #ofilevariablelist=ifile+ ".var"
        #ofilevariablelist= os.path.join("testout","test.pt.tok.tc.var")
        print (myFile) 
        # importnat reverse order than
        print ("Starting variable replenishment...")        
        variable_replenishment(ifile,ofiletmp,ofilevariablelist)
        #
        print ("Detokenizing the fie...")        
        normalize_detokenize_file(ofiletmp,ofile1)
        # now our changes
        # numbers to NN
        
                


if __name__ == '__main__':
    interactive=True    
    vprinta=0
    print ("Current working dir ", os.getcwd())
    
    args = docopt(__doc__)
    print (args)

    myFileList=[]   
    tagcasing=True # default
    varnum=True
    
    if args["tokenize"]:
        srcfile=args["--src"]
        tokfile=args["--tokfile"]
        myFileList.append(srcfile)
        tgtfile=args["--tgt"]
        if tgtfile!=None:
            myFileList.append(tgtfile)
        tokenlist=tokfile
        tagcasing=eval(args["--tagcasing"])
        varnum=eval(args["--varnum"])
        f_main_tokeniza(myFileList,tagcasing, tokenlist, varnum)
    elif args["detokenize"]:
        srcfile=args["--src"]
        varfile=args["--varfile"]
        myFileList.append([srcfile,varfile]) 
        f_main_detokeniza(myFileList)
    elif args["toklist"]:
        corpusfile=args["--corpus"]
        tokfile=args["--tokfile"]
        normalize_tokenize_file(corpusfile, tokfile, "CREATELIST")
        
   #### example o tokenization and detokization
    #         
    #myFileList=[]   
    #myFileList.append(os.path.join("..","03_data","UNv1.0.en-fr.en.shf.ddup.c4"))    
    #myFileList.append(os.path.join("..","03_data","UNv1.0.en-fr.fr.shf.ddup.c4"))    
    #   
    #tokenlist=os.path.join("..","03_data","list.tkl")                    
    #tagcasing= True


    #f_main_tokeniza(myFileList,tagcasing, tokenlist)
   
   ################################
    ################################
    #### detokenize ################
    # PT ES
    #tokenlist=os.path.join("..","00_mono","data4","clean.tkl")                    
    #myFileList=[]           
    #myFileList.append([os.path.join("pt.dtk.clean.2.tok.tc.sp.2es.dec"), 
    #                   os.path.join("pt.dtk.clean.2.tok.tc.var")] )
    #myFileList=[]           
    #myFileList.append([os.path.join("pt.dtk.clean.3.5.2.tok.tc.sp.2es.dec"), 
    #                   os.path.join("pt.dtk.clean.3.5.2.tok.tc.var")] )
    #tagcasing= True
    
    #f_main_detokeniza(myFileList)
  
  

   
    print ("EOP.")

