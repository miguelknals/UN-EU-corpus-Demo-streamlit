import streamlit as st
import sentencepiece as spm
import ctranslate2
import pandas as pd
import math
# mine
import Simple_DETOK
import Simple_TOK


@st.cache_data
def translation_function(lang_pair, sources):
    # load models
     # Load models
    translator, sp_source_model, sp_target_model = load_models(lang_pair, device="cpu")
    # we can start the translation process
    # first detokenize the source
    wkging_dir="workdir/"
    # need to create a tmp file for transaltion stream
    src_file= wkging_dir + "source.txt"
    with open (src_file, encoding='utf-8', mode ='w') as ofile:
        for l in sources:
            ofile.write("{}\n".format(l))
    # tokenize with tagcasig and no num variables
    Simple_TOK.func_main_process(src_file)
    # this will generate source.txt.tok
    # now we need sp. 
    # we need to read the sp file
    s_ifile1= src_file + ".tok"
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
    with open(s_ifile1+".sp", encoding='utf-8', mode ='w') as ifile1:
        for s in sp_bpe_list:
            l=""
            for w in s:
                l+=" " + w
            ifile1.write("{}\n".format(l))
        
    sp_bpe_translated_list=[] # results
    sp_bpe_translated_list_scores=[]
    TranslationResult_list=[] 
    TranslationResult_list = translator.translate_batch(sp_bpe_list, return_scores=True)
    # for debug
    with open(s_ifile1+".sp.2tgt.sp", encoding='utf-8', mode ='w') as ifile1:
        for TranslationResult in TranslationResult_list:
            tgt_sentence=TranslationResult.hypotheses[0]
            l=""
            for w in tgt_sentence:
                l+=" "+ w
            ifile1.write("{}\n".format(l))
    
    
     
    
    for TranslationResult in TranslationResult_list:
        tgt_sentence=TranslationResult.hypotheses[0]
        tgt_sentence_score=TranslationResult.scores[0]
        aux=len(tgt_sentence)
        if aux==0:
            aux=1
        tgt_sentence_score_average=math.exp(TranslationResult.scores[0]/aux)*100
        print(tgt_sentence)
        print(tgt_sentence_score)
        sp_bpe_translated_list.append(tgt_sentence) # translation
        sp_bpe_translated_list_scores.append(tgt_sentence_score_average ) # scores
    # now se need to decode
    target_list_tk=sp_target_model.decode(sp_bpe_translated_list)
    # now need to normalize
    s_ifile1= src_file + ".tok.2tgt" # from .tok.2tgt.sp to .tok.2tgt
    with open(s_ifile1, encoding='utf-8', mode ='w') as ifile1:
        for l in target_list_tk:
            ifile1.write("{}\n".format(l)) 
    # now lets call again to ee_normaliza
    Simple_DETOK.func_main_process(s_ifile1 )
    # 
    # last step read the file
    s_ifile1= src_file + ".tok.2tgt.detok"
    final_translated_list= []
    with open(s_ifile1, encoding='utf-8', mode ='r') as ifile1:
        while True:
            l1 = ifile1.readline().lstrip("\n")            
            final_translated_list.append(l1)
            print (l1)
            if not l1:
                break
            
    return final_translated_list, sp_bpe_translated_list_scores


    

    return

@st.cache_resource
def load_models(lang_pair, device="auto"):
    if lang_pair == "English-to-French":
        ct_model_path = "enfr_ctranslate2/"
        sp_source_model_path = "spm/bpe.model"
        sp_target_model_path = "spm/bpe.model"
    elif lang_pair == "French-to-English":
        ct_model_path = "fren_ctranslate2/"
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
    st.title("EN<>FR Machine Translation (MT) - United Nations and European Community corpora") 
    st.write("##### UN-EUR-MT is a working MT for ENG<>FRE based on the UN bilingual corpus and several other smaller corpora from the European Union. All these corpora have been cleaned.")
    st.write("Visit the [UN-EU-corpus-Demo-streamlit](https://github.com/miguelknals/UN-EU-corpus-Demo-streamlit/tree/main) repository for more information.  ")
    st.write("You can visit the [United Nations Official Document System](https://documents.un.org/prod/ods.nsf/home.xsp)  to grab an example.")
    #if st.checkbox('Show some notes...'):
    #    st.write('''
    #             ## Notes
    #             - This is a demo of a Streamlit app.
    #             - This is using **st.cache**.
    #             - This will be deployed to Heroku.                 
    #            ''')
    with st.form("my_form"): # need to add a button
        # Dropdown
        lang_pair = st.selectbox("##### Select Language Pair",
                                ("English-to-French", "French-to-English"))
        # input text 
        def_text= "United Nations S/2023/994\n"
        def_text+="Security Council Distr.: General\n"
        def_text+="15 December 2024\n"
        def_text+="Original: English\n"
        def_text+="23-25457 (E) 211223\n"
        def_text+="*2325457*\n"
        def_text+="Letter dated 15 December 2023 from the Permanent Representative of Pakistan to the United Nations addressed to the President of the Security Council\n" 
        def_text+="I have the honour to transmit herewith a letter dated 14 December 2023 from the Foreign Minister of Pakistan, Jalil Abbas Jilani, addressed to you regarding the situation in disputed Jammu and Kashmir (see annex).\n"
        def_text+="I would like to request that the present letter and its annex be circulated as a document of the Security Council in connection with the item entitled ""The India - Pakistan question""."
        
        user_input = st.text_area("##### Enter your source text (Plain text without tags - ONE sentence per line - Max aprox 250 lines - NO GPU - aprox 1-2 seconds x sentence):", 
                                  max_chars=30000, value=def_text,height=250) 
        # process input text
        sources = user_input.split("\n")  # split on new line.
        if len (sources) != 1 or sources[0].strip() != "":
        #    # there is something to translate
            final_translated_list, scores_list=translation_function(lang_pair, sources)
            df = pd.DataFrame({ 
            'Pred:': scores_list[0:len(sources)],
            'Source': sources,
            'Target': final_translated_list[0:len(sources)]
            } )
            st.write("## Translation table")
            #pd.set_option('display.index', False)
            df2=df.iloc[:, 1:] # removing Pred:
            st.table(df2.set_index(df2.columns[0]))
            #st.table(df.set_index(df.columns[0]))
            st.write("### Data download")
            st.write("-You can download the results as a CSV file")
            st.write("-Pred. score is the average of the neg log likelihood of the translation (there is not an easy correlation with translation quality or confidence)")
            st.dataframe(df, use_container_width=True)
            
        
        st.write("Number of lines: {} (aprox 1-2 sec x sentence)".format(len(sources)))               
        # Create a button
        submitted = st.form_submit_button("Translate")
    st.write("(c) 2024 miguelknals - MIT License")
    

if __name__ == "__main__":
    
    main()
    
    # debug code
    sources=["1.1 L’auteur de la communication est G. S.",
"1.1 L’auteur de la communication est G. S., de nationalité roumaine.",
"1.1 L’auteur de la communication est G. S., de nationalité roumaine, né en 1962. "]
    sources=["1.1 The author of the communication is G.S. a national of Romania, born in 1962. "]
    #final_translated_list=translation_function("English-to-French",sources)
    #for tgt in final_translated_list:
    #    print(tgt)
        
    

    
