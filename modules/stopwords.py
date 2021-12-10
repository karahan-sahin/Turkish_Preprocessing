
###################
# STOPWORD REMOVAL
###################
from typing import Text
from Turkish_Preprocessing.utils_ import import_corpora
from collections import defaultdict
import math
import re
from Turkish_Preprocessing.modules.tokenizer import Tokenizer
import itertools

class StopwordRemoval():

    def __init__(self, type="lexicon", top_k=100):
        self.top_k = top_k
        self.type = type

        self.corpus = import_corpora(type="stopwords")
        
        if self.type == "lexicon":
            self.import_stopwords()
        
        elif type == "custom":
            self.dynamic()
        
        
    def remove(self,tokenized_text):
        """
        
        -i
        """
        return [token for token in tokenized_text if not (token in self.stopwords)]

    def dynamic(self):
        """
        Input: 90000+ randomly collected Sinhala text documents
            Procedure Avg_TF_IDF_Score (input):
            1. Calculate the term frequency (TFt, d) for each word
            in the document.
            2. Parallelly calculate the document frequency (DF)  of each word in the corpus.
            3. After calculating the document frequency, calculate
            the Inverse document frequency (IDFt) with the
            count of documents N in the given source text.
            4. Calculate TF-IDF score for each word.
            5. Average_TF-IDFt = TF-IDFt, d / count (t)
            6. Order Average_TF-IDFt score in ascending order.  
        """
        count_dict = defaultdict(int)
        tf_dict = defaultdict(dict)
        for idx,doc in enumerate(self.corpus):
            doc = [token for token in doc if token.isalnum()]
            doc_dict = defaultdict(int)
            for token in doc:
                token = token.lower()
                doc_dict[token] += 1 
            for token in set(doc):
                token = token.lower()
                count_dict[token] += 1
            tf_dict[idx] = doc_dict

        idf_dict = {word: math.log10(len(self.corpus)/count) for word,count in count_dict.items()}

        tfidf_dict = defaultdict(int)
        for doc in tf_dict.values():
            for token, count in doc.items():
                tfidf_dict[token] += (count * idf_dict[token]) / count_dict[token]

        sorted_tfidf = dict(sorted(tfidf_dict.items(), key=lambda item: item[1]))

        self.stopwords = list(sorted_tfidf.keys())[:self.top_k]


    def import_stopwords(self):
        self.stopwords = list(open("source/stopwords/stopwords.txt", 'r', encoding='utf-8').read().split('\n'))