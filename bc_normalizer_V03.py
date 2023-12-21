
"""
Usage:
    bc_normalizer_V03 toklist --corpus=<file> --tokfile=<file> 
    
Options:
    -h --help                               show this screen.
    --corpus=<file>                         corpus file (use with toklist command)
    --tokfile=<file>                        tokens file (use with toklist option)
"""


from docopt import docopt

# this programs reads:
# C:\u_M\05_T4T\02_py\00_mono\dataeuroparl-v10.es.txt
# and normalizes and tokenizes with sacremoses
import os
import unicodedata
# from sacremoses import MosesTokenizer, MosesDetokenizer, MosesPunctNormalizer
ja="￭"
ja="@@"

    

def normalize_tokenize_file(ifile, ofile1,tokenlistfile):
    """ Main    
    """

    searchchars=""
    bool_CreateList= False
    if (tokenlistfile == "CREATELIST"):
        tokenlistfile=ifile+".tkl"
        tokenlistfile= ofile1 # v3 change
        print ("A token list will be created")
        print ("File "+ tokenlistfile)
        bool_CreateList=True # we will create a token list file

    global vprinta    
    vprinta =0
    
    counter=999e6 # es de debug para leer solo 1000 líneas
    #counter=1000000
    rdl=0
    wrl=0
    dic={}
    ofilelog=ofile1+".err"
    with  open(ifile,  encoding='utf-8', mode='r', errors="ignore") as i1, \
          open(ofile1, encoding='utf-8',mode='w') as o1, \
          open(ofilelog, encoding='utf-8',mode='w') as olog:

        if bool_CreateList== False:
            with open(tokenlistfile, encoding='utf-8',mode='r') as otoklist:
                # we have a token list file
                while True:
                    l = otoklist.readline()
                    if not l:
                        break
                    l=l.rstrip("\n")
                    searchchars+=l
            #searchchars+="“”’‘"


        while True:
            printa()            
            rdl+=1 # es de debug para leer solo 1000 líneas
            if (counter == rdl ):
                break
            l = i1.readline()
            if not l:
                break
            #if rdl==8321: # debug
            #    print()
            l=l.rstrip("\n")
                
            lonl=len(l)
            l2="" # new line with tokenized symbols list
            for i in range (0,lonl):
                aux=l[i]
                boolproces=False
                if (aux.isalpha()==True or aux ==" " or aux.isdigit()==True):
                    # nothing to todo
                    boolproces=True 

                if boolproces== False:  #next find out if this is hyphen
                    for cs in searchchars:
                        if cs==l[i]:
                            boolproces= True
                            aux=" "
                            if i>0 and l[i-1] !=" ":
                                aux+=ja
                            aux+=l[i]
                            if i < lonl-1 and l[i+1] != " ":
                                aux+=ja
                                aux+=" "
                                boolproces= True
                            #aux="" # this line in order to do not print @@ items
                            break # no need to search more

                    if boolproces ==False:    # char live ? if not yet processed
                        if (aux.isprintable()== False):
                            # this is control char
                            aux=""
                            boolproces= True
                        
                    # still not processed, we have a new printable char not
                    # in our special char variable
                    if boolproces == False: # looks we have not process char   
                        #print (l)
                        token=l[i]
                        if token in dic:
                            dic[token]+=1
                        else:
                            dic[token]=1
                            
                l2+=aux
                    



            # need to remove extra blanks
            # do not create file if we are creating the tag list
            if bool_CreateList==False:
                auxl=l2.split()
                l2=" ".join(auxl)
                if l2.strip()=="":
                    l2="error"
                o1.write(l2 + "\n") 
            # 
        # https://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-a-value-of-the-dictionary
        # now the dictionary
        dic_sorted = sorted(dic, key=dic.get, reverse=True)
        for r in dic_sorted:
            olog.write (r +" " +str(dic[r])+ "\n")
            
        if bool_CreateList:
            with open(tokenlistfile, encoding='utf-8',mode='w') as otoklist:
                for r in dic_sorted:
                    otoklist.write(r+"\n")


          

    

               
    print  ("EOP")



def normalize_detokenize_file(ifile, ofile1):
    """ Main    
    """
    global vprinta
    vprinta =0
    counter=999e6 # es de debug para leer solo 1000 líneas
    rdl=0
    wrl=0

    
    with  open(ifile,  encoding='utf-8', mode='r' ) as i1, \
          open(ofile1, encoding='utf-8',mode='w') as o1:
          # open(ofile2, encoding='utf-8',mode='w') as o2:
        while True:
            printa()            
            rdl+=1 # es de debug para leer solo 1000 líneas
            if (counter == rdl ):
                break
            l = i1.readline()
            if not l:
                break                        
            
            l=l.replace(" "+ja,"")
            l=l.replace(ja+" ","")
            l=l.replace(ja,"")
            o1.write( l ) 
    
    

               
    print  ("EOP")



def printa():
    # need to use vprinta = 0 at the start of main
    global vprinta
    vprinta+=1
    if (vprinta % 5000==0):
        print (".", end ="")  
    if (vprinta % 100000==0):
        print (" ", vprinta)


def main_token():
    
    #vprinta=0
     #myfile = os.path.join("data","corpus_PARTIAL.tok.txt")


    ofile2=  os.path.join("datapt","corpus.pt.tok.error.txt")
    ifile=  os.path.join("..","02_bitext", "dataout","europarl-v10.es.pair.txt")
    ofile1=  os.path.join("..","02_bitext", "dataout","europarl-v10.es.tok.txt")
    ofile1= os.path.join("data2","test.es.tok")
    ifile=  os.path.join("data2","corpus.shuf.es")
    ofile1=""
    ifile=  os.path.join("..","02_bitext","data","test.es")
    ifile = os.path.join("data3","pt.corpus")    

    ifile = os.path.join("..","02_bitext","data","dev.pt")
    ifile=  os.path.join("..","02_bitext","data","test.es")    
    
    ifile=  os.path.join("data3","mono.pt.corpus")        

    ifile=  os.path.join("data3","mono.es.corpus")        


    ifile=  os.path.join("..","02_bitext","data2","dev.ca")     
    toklist =   os.path.join("data4","list.tkl_mono")     
    #normalize_tokenize_file(ifile, ifile+".tok", toklist)
    

    # instructions. First tok list must be "CREATELIST"
    # this sill generate a list of the tokenizing symbols
    # to be annoted. The file will be named with the extension
    # tkl (Token list). This file later can be renamed to i.e.
    # list.tkl that will be useed in a no creating pahse
    # (the err file that is created (TildeMODEL.dtk.es.corpustok.err)
    # usually should be empty (otherwise means there is a token
    # not coirrectly sentenced. 
    # Example 1st run  (only first time)
    #
    #  ifile=  os.path.join("data","TildeMODEL.dtk.es.corpus")        
    #  normalize_tokenize_file(ifile, ifile+".tok", "CREATELIST")
    #
    # this will create TildeMODEL.dtk.es.corpus.tkl
    # we rename this file as list.tkl and run
    #
    # ifile=  os.path.join("data","TildeMODEL.dtk.es.corpus")     
    # toklist =   os.path.join("data","list.tkl")     
    # normalize_tokenize_file(ifile, ifile+".tok", toklist)
    #
    # this will generate a corrected tokenized file:
    # TildeMODEL.dtk.es.corpus.tokcd 
    # notice that TildeMODEL.dtk.es.corpus.tok.err should be empty

    #ifile=  os.path.join("..","00_mono","data5","mono")     
    #normalize_tokenize_file(ifile, ifile+".tok", "CREATELIST")
    #
    #ifile=  os.path.join("data4","tmp","mono2.es.ddp")     
    #toklist =   os.path.join("data4","list.tkl_mono")     
    #normalize_tokenize_file(ifile, ifile+".tok", toklist)
    #

    #ifile=  os.path.join("..","03_data","UNv1.0.en-fr")        
    #normalize_tokenize_file(ifile, ifile+".tok", "CREATELIST")
    #
    ifile=  os.path.join("..","03_data","UNv1.0.en-fr.en.10K.clean")        
    toklist =   os.path.join("..","03_data","list.tkl")     
    normalize_tokenize_file(ifile, ifile+".tok", toklist)

    
    # destokeniza(ifile+ ".tok", ifile + ".back")

    print ("EOP")


def main_detoken():
    ifile=  os.path.join("..", "00_mono","data","toktest.txt.tok.debug")     
    normalize_detokenize_file(ifile,ifile+".dtk")
    print ("EOP.")
    
  


if __name__ == '__main__':
    # this program is mainly used a a function repository
    # most of the time classes are called from ee_normalize 
    # this program is intersting if you want to tokenize 
    # a single file only something you cannot to with 
    # ee_normalize that requires src-tgg
    args = docopt(__doc__ )
    print(args)
    
    # for token list
    if args["toklist"]:
        corpus=args["--corpus"]
        tokfile=args["--tokfile"]
        #normalize_tokenize_file(corpus, corpus+".tok", "CREATELIST")
        normalize_tokenize_file(corpus, tokfile, "CREATELIST")

    #for detokenzie
    #main_detoken()
    
    #for tokenize
    #main_token()

    
