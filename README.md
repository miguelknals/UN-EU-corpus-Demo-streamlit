# EN<>FR Machine Translation (MT) based on cleaned United Nations and European Union corpora (UN-EUR-MT)

This a working MT for ENG<>FRE based on the UN bilingual corpus and several other smaller corpora from the European Union. All these corpora have been cleaned with:

- Physical cleaning (custom scripts i.e. removing lines with more than 1 sentence, text between parenthesis)
- Semantical filtering based on Unbabel COMET score with the reference free model Unbabel/wmt22-cometkiwi-da

This has assured that the corpora have good quality and with probably very few few unalignment sentences or very disimilar sentences. Final corpora has total size of aprox 22.14M sentences/ 558M words.

We have used OpenNMT toolkit, to replicate the Google's transformer model. 

This repository has been designed to be deployed in streamlit as a public application  -> https://un-eu-corpus-demo.streamlit.app/

## UN-EUR-MT BLEU scoring

We have used 3 pair texts and we have run the UN-EUR-MT and Google translator, in each case, we use as reference, the translation provided for these examples.

#### UNv1.0.testset from the UN corpus paper (The United Nations Parallel Corpus v1.0 paper) 10.6K eng words

Lang  | UN Moses (ref.)  |  UN-EUR-MT | GOOGLE
------------- | -------------| -------------| -------------
EN->FR  | 50.33| **49.13** | 44.46
FR->EN  | 52.58 | **50.88** | 45.27

#### Random sample UN resolution ( RESOLUTION 2713 (2023) /ADOPTED BY THE SECURITY COUNCIL AT ITS 9490TH MEETING, ON 1 DECEMBER 2023) 5.3K eng words
Lang  |   UN-EUR-MT | GOOGLE
------------- | -------------| -------------
EN->FR  | **42.00**| 41.25
FR->EN  |  **45.89** | 44.62

#### Random sample EU ( Official Journal of the European Union, C 049, 9 February 2023 -  product specification for a name in the wine sector)
Lang  |   UN-EUR-MT | GOOGLE
------------- | -------------| -------------
EN->FR  | 26.19|  **33.48**
FR->EN  |  24.81 | **30.20**

Note: This file probably is not very representative from other UN/EU texts, as is related to the wine sector. The purpose of this demo is show you can beat Google in specific domains (but probably not as a general purpose MT)

## Conclusions

- Remember BLEU score is just a statistical score, that troubles with NMT models in terms of fluency and construction.
- UN-EUR-MT probably is better for legal/UN/EU texts than Google (according BLEU by a small margin) , but lags behind in more general contexts (the wine sector test file)
- Probably additional analysis has to be done to decide a "winner" if any. 

## United Nations and European Community corpora used

The following corpus have been used:

- United Nations Parallel Corpus 1990-2014 Eng-Fre (UNv1.0.en-fr.fr.ddup.c2.100.c3 aprox 25M lines, after cleaning 15.85M) 
- European Parliament Proceedings Parallel Corpus 1996-2011 Eng-French (europarl-v7.fr-en.en.ddup.c2.100.c3 aprox 2.0M sentences, after cleaning 1.75M )
- Digital Corpus of the European Parliament 2013 EN-FR  (DCEP-FR.ddup.c2.100.c3, apro 5.8M  aprox, after cleaning 1.41M sentences
- Joint Research Centre (JRC)- Acquis Communautaire (JRC-Acquis.3.0) (JRC-Acquis.en-fr.fr.ddup.c2.100.c3 aprox 800K, after cleaning 407K sentences)
- European Commission's Directorate-General for Translation - Translation Memory (DGT-TM) (Euro-en-fr.txt.fr.ddup.c1.100.c3 aprox 6.72M, after cleaning 3.23M sentences) 

UN sources counts aprox 70%, EU sources 30%. Total corpus size 22.6M sentences

Once joined and removing duplicates, **total size of the corpus used for this TM is aprox 22.14M sentences/ 558M words**.


## References and notes:

### Notes:
- This page has been partly based on CTranslate-NMT-Web-Interface (https://github.com/ymoslem/CTranslate-NMT-Web-Interface).
- This repository has been created solely in my free time, belongs exclusively to me and has not been sponsored by any organization

### Refs:
OpenNMT -> https://opennmt.net/

Attention is all you need (Transformer model) -> https://arxiv.org/abs/1706.03762

Unbabel/wmt22-cometkiwi-da -> https://huggingface.co/Unbabel/wmt22-cometkiwi-da

Unbabel COMET score -> https://github.com/Unbabel/COMET

United Nations Parallel Corpus -> https://conferences.unite.un.org/uncorpus

The United Nations Parallel Corpus v1.0 -> https://conferences.unite.un.org/uncorpus/Content/Doc/un.pdf

European Parliament Proceedings Parallel Corpus -> https://www.statmt.org/europarl/

Digital Corpus of the European Parliament -> https://wt-public.emm4u.eu/Resources/DCEP-2013/DCEP-extract-README.html

Joint Research Centre (JRC)- Acquis Communautaire (JRC-Acquis.3.0) -> https://joint-research-centre.ec.europa.eu/language-technology-resources/jrc-acquis_en

European Commission's Directorate-General for Translation - Translation Memory -> https://joint-research-centre.ec.europa.eu/language-technology-resources/dgt-translation-memory_en


(c) miguel canals, 2024 - miguelknals - www.mknals.com
