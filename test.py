import streamlit as st
import ee_normaliza as mytokdetok
import sentencepiece as spm
import ctranslate2 as ct

def main():
    st.write ("""
              
              # Simple Stock Price App
              
              """)
    
    
    tickerSymbol = 'STG.AX'
    tickerData= yf.Ticker(tickerSymbol)
    
    tickerDf= tickerData.history(period='1d', start='2020-5-31', end='2023-12-12')
    
    st.line_chart(tickerDf.Close)
    print (tickerDf.Close)
    st.line_chart(tickerDf.Volume)
    st.write ("Data loaded from Yahoo Finance")
    
def translate(source, translator, predict_score = False):
    """Use CTranslate model to translate a sentence

    Args:
        source (str): A source sentence to translate
        translator (object): Ctransalte2 object 
        predict_score: Indicate if you want the predict score outputted with the translation.

    Returns:
        Translation of the source text.
    """

    TranslationResult_list=[]
    TranslationResult_list = translator.translate_batch(source, return_scores=predict_score)
    
    return TranslationResult_list

    
if __name__ == "__main__":
    #main()
    ct_model="UN-EU-100K.pt"
    src_file= "tranfolder\\EURO-UN.en.01.10.txt"
    myFileList= []
    myFileList.append(src_file)
    tokenlist= "list.tkl"
    tagcasing=True
    varnum= False
    # tokenize with tagcasig and no num variables
    mytokdetok.f_main_tokeniza(myFileList,tagcasing, tokenlist, varnum)
    # this will generate src.tok.tc
    #                    src.tok.tc.var
    # now we need sp. 
    # we need to read the sp file
    s_ifile1= src_file + ".tok.tc"
    var_file= src_file + ".tok.tc.var"
    sp_source_list= []
    with open(s_ifile1, encoding='utf-8', mode ='r') as ifile1:
        while True:
            l1 = ifile1.readline()
            sp_source_list.append(l1)
            if not l1:
                break

    sp = spm.SentencePieceProcessor(model_file='spm\\bpe.model')
    sp_bpe_list=sp.encode_as_pieces(sp_source_list)
    # need to add sp.bos_id() and sp.eos_id()
    for s in sp_bpe_list:
        s.append("</s>")
        s.insert(0,"<s>")
    # now we ctranslate
    
    sp_bpe_translated_list=[]
    translator = ct.Translator(ct_model, device='auto') # device='cpu' or 'cuda' or 'auto'¿
    TranslationResult_list = translate(sp_bpe_list, translator, predict_score=True)
    for TranslationResult in TranslationResult_list:
        print(TranslationResult[0]["tokens"])
        print(TranslationResult[0]["score"])
        sp_bpe_translated_list.append(TranslationResult[0]["tokens"] )
    # now se need to decode
    target_list_tk=sp.decode(sp_bpe_translated_list)
    # now need to normalize
    s_ifile1= src_file + ".tok.tc.2fr"
    with open(s_ifile1, encoding='utf-8', mode ='w') as ifile1:
        for l in target_list_tk:
            ifile1.write("{}\n".format(l)) 
    # now lets call again to ee_normaliza
    myFileList=[]  
    myFileList.append([s_ifile1,var_file])
    mytokdetok.f_main_detokeniza(myFileList)
    # 
    # last step read the file
    s_ifile1= src_file + ".tok.tc.2fr.dtok.4cl"
    final_translated_list= []
    with open(s_ifile1, encoding='utf-8', mode ='r') as ifile1:
        while True:
            l1 = ifile1.readline()            
            final_translated_list.append(l1)
            print (l1)
            if not l1:
                break

    
    # test
    
    
    print ("EOP")
