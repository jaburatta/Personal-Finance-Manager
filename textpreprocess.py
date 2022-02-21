# import necessary libraries
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import spacy
import string
from spacy.lang.en import English
from spacy.lang.en.stop_words import STOP_WORDS
import re

## Load Spacy English Model for NLP
nlp = spacy.load('en_core_web_sm')

## Instantiate punctuation from string module and stopwords from spacy
punctuations = string.punctuation

### New stop words
new_words = [
    "buhari", 
    "babangida", 
    'osinbajo',
    'osibanjo',
    'boris',
    'johnson,',
    'sunday',
    'john',
    'doe',
    'abdul',
    'tafawa',
    'balewa',
    'bukola',
    'saraki',
    'habibi'
]

STOP_WORDS.update(new_words)
stopwords = list(STOP_WORDS)

class TextProcessingTransformer(BaseEstimator, TransformerMixin):
    
    def __init__(self, X=None, y = None):
        self.X = X
        self.y = y
        
    def fit(self, X, y = None):
        return self

    def transform(self, X, y = None):

        '''
        This method preprocesses texts in order to get a normalized string
        '''
        X = pd.Series(X)
        for i in X.index:

            text_wo_urls = re.sub(r'http\S+', ' ', X[i])

            # remove mentions(@) if present in text
            text_wo_mentions = re.sub(r'@\w+', ' ', text_wo_urls)

            # remove hash-tags(#) if present in text
            text_wo_tags = re.sub(r'#\w+',' ', text_wo_mentions)

            # remove special characters({ ^ % \ ~ / ) if present in text 
            text = re.sub('[^A-Za-z]+', ' ', text_wo_tags)

            # using spacy english model to parse text
            tokens = nlp(text)

            # lemmatize tokens to their original words
            tokens = [token.lemma_.lower().strip() for token in tokens]

            # Filter out relevant tokens i.e tokens not in stopwords, tokens not in punctuation and token > 2 (bcos of words like ATM, POS, WEB) 
            toks = [token for token in tokens if token not in stopwords and token not in punctuations and len(token)>2]

            X[i] = " ".join(toks)

        return X