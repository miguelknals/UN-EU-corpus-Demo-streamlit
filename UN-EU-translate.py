import streamlit as st
import sentencepiece as spm
import ctranslate2
import ee_normaliza as mytokdetok
import pandas as pd




@st.cache_data
def translation_function(lang_pair, sources):
    # load models
     # Load models
    translator, sp_source_model, sp_target_model = load_models(lang_pair, device="cpu")
    # we can start the translation process
    # first detokenize the source
    wkging_dir="workdir/"
    tokenlist= "list.tkl"
    tagcasing=True
    varnum= False
    # need to create a tmp file for transaltion stream
    src_file= wkging_dir + "source.txt"
    with open (src_file, encoding='utf-8', mode ='w') as ofile:
        for l in sources:
            ofile.write("{}\n".format(l))
    myFileList= []
    myFileList.append(src_file)
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

    sp_bpe_list=sp_source_model.encode_as_pieces(sp_source_list)
    # need to add sp.bos_id() and sp.eos_id()
    for s in sp_bpe_list:
        s.append("</s>")
        s.insert(0,"<s>")
    # now we ctranslate
    sp_bpe_translated_list=[] # results
    TranslationResult_list=[] 
    TranslationResult_list = translator.translate_batch(sp_bpe_list, return_scores=True)
    
    for TranslationResult in TranslationResult_list:
        print(TranslationResult.hypotheses[0])
        print(TranslationResult.scores[0])
        sp_bpe_translated_list.append(TranslationResult[0]["tokens"] )
    # now se need to decode
    target_list_tk=sp_target_model.decode(sp_bpe_translated_list)
    # now need to normalize
    s_ifile1= src_file + ".tok.tc.2tgt"
    with open(s_ifile1, encoding='utf-8', mode ='w') as ifile1:
        for l in target_list_tk:
            ifile1.write("{}\n".format(l)) 
    # now lets call again to ee_normaliza
    myFileList=[]  
    myFileList.append([s_ifile1,var_file])
    mytokdetok.f_main_detokeniza(myFileList)
    # 
    # last step read the file
    s_ifile1= src_file + ".tok.tc.2tgt.dtok.4cl"
    final_translated_list= []
    with open(s_ifile1, encoding='utf-8', mode ='r') as ifile1:
        while True:
            l1 = ifile1.readline().lstrip("\n")            
            final_translated_list.append(l1)
            print (l1)
            if not l1:
                break
            
    return final_translated_list


    
    

    return

@st.cache_resource
def load_models(lang_pair, device="auto"):
    if lang_pair == "English-to-French":
        ct_model_path = "UN-EU-100K-EN2FR.pt/"
        sp_source_model_path = "spm/bpe.model"
        sp_target_model_path = "spm/bpe.model"
    elif lang_pair == "French-to-English":
        ct_model_path = "UN-EU-100K-FR2EN.pt/"
        sp_source_model_path = "spm/bpe.model"
        sp_target_model_path = "spm/bpe.model"

    sp_source_model = spm.SentencePieceProcessor(sp_source_model_path)
    sp_target_model = spm.SentencePieceProcessor(sp_target_model_path)
    translator = ctranslate2.Translator(ct_model_path, device)
    
    return translator, sp_source_model, sp_target_model
    

def main():
    st.set_page_config(page_title="EN<>FR UN-Euro corpus MT",
                       layout="wide",
                       page_icon="✨")
    st.title("MT UN-Euro corpus EN<>FR")
    st.write("Welcome to my app!")
    if st.checkbox('Show some notes...'):
        st.write('''
                 ## Notes
                 - This is a demo of a Streamlit app.
                 - This is using **st.cache**.
                 - This will be deployed to Heroku.                 
                ''')
    with st.form("my_form"): # need to add a button
        # Dropdown
        lang_pair = st.selectbox("Select Language Pair",
                                ("English-to-French", "French-to-English"))
        # input text 
        user_input = st.text_area("Source Text", max_chars=2000)
        # process input text
        sources = user_input.split("\n")  # split on new line.
        if len (sources) != 1 or sources[0].strip() != "":
        #    # there is something to translate
            final_translated_list=translation_function(lang_pair, sources)
            df = pd.DataFrame({ 
            'Source': sources,
            'Target': final_translated_list[0:len(sources)]
            } )
            st.dataframe(df, use_container_width=True)
        
        st.write("Number of lines: {}".format(len(sources)))               
        # Create a button
        submitted = st.form_submit_button("Translate")

if __name__ == "__main__":
    
    main()
    
    # debug code
    #sources=["To be held on Tuesday, 12 May 2015, at 3 p.m.", "2015 session"]
    #final_translated_list=translation_function("English-to-French", sources)
    #for tgt in final_translated_list:
    #    print(tgt)
        
    

    
