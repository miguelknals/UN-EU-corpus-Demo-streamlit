import streamlit as st
import sentencepiece as spm
import ctranslate2
import ee_normaliza as mytokdetok


def get_source():
    #main()
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
    
    return sp_bpe_list



def translate(source, translator, sp_source_model, sp_target_model):
    """Use CTranslate model to translate a sentence

    Args:
        source (str): Source sentences to translate
        translator (object): Object of Translator, with the CTranslate2 model
        sp_source_model (object): Object of SentencePieceProcessor, with the SentencePiece source model
        sp_target_model (object): Object of SentencePieceProcessor, with the SentencePiece target model
    Returns:
        Translation of the source text
    """

    #source_sentences = sent_tokenize(source)  # split sentences
    #source_tokenized = sp_source_model.encode(source_sentences, out_type=str)
    #translations = translator.translate_batch(source_tokenized, replace_unknowns=True)
    translations = translator.translate_batch(source, replace_unknowns=True)
    translations = [translation[0]["tokens"] for translation in translations]
    translations_detokenized = sp_target_model.decode(translations)

    return translations_detokenized


# [Modify] File paths here to the CTranslate2 and SentencePiece models.
@st.cache(allow_output_mutation=True)
def load_models(lang_pair, device="cpu"):
    """Load CTranslate2 model and SentencePiece models

    Args:
        lang_pair (str): Language pair to load the models for
        device (str): "cpu" (default) or "cuda"
    Returns:
        CTranslate2 Translator and SentencePieceProcessor objects to load the models
    """
    if lang_pair == "English-to-French":
        ct_model_path = "UN-EU-100K.pt\\" # this is a directory
        sp_source_model_path = "spm\\bpe.model"
        sp_target_model_path = "spm\\bpe.model"
    #elif lang_pair == "French-to-English":
    #    ct_model_path = "/path/to/your/ctranslate2/model/"
    #    sp_source_model_path = "/path/to/your/sp_source.model"
    #    sp_target_model_path = "/path/to/your/sp_target.model"

    sp_source_model = spm.SentencePieceProcessor(sp_source_model_path)
    sp_target_model = spm.SentencePieceProcessor(sp_target_model_path)
    translator = ctranslate2.Translator(ct_model_path, device)

    return translator, sp_source_model, sp_target_model


# Title for the page and nice icon
st.set_page_config(page_title="NMT", page_icon="🤖")
# Header
st.title("Translate")

# Form to add your items
with st.form("my_form"):

    # Dropdown menu to select a language pair
    lang_pair = st.selectbox("Select Language Pair",
                             ("English-to-French", "French-to-English"))
    # st.write('You selected:', lang_pair)

    # Textarea to type the source text.
    user_input = st.text_area("Source Text", max_chars=200)
    sources = user_input.split("\n")  # split on new line.

    # Load models
    translator, sp_source_model, sp_target_model = load_models(lang_pair, device="cpu")

    # Translate with CTranslate2 model
    source= get_source()
    translations = [translate(source, translator, sp_source_model, sp_target_model) for source in sources]
    translations = [" ". join(translation) for translation in translations] 

    # Create a button
    submitted = st.form_submit_button("Translate")
    # If the button pressed, print the translation
    if submitted:
        st.write("Translation")
        st.code("\n".join(translations))


# Optional Style
st.markdown(""" <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .reportview-container .main .block-container{
        padding-top: 0rem;
        padding-right: 0rem;
        padding-left: 0rem;
        padding-bottom: 0rem;
    } </style> """, unsafe_allow_html=True)


