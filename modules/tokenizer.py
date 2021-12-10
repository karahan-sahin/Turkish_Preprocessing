from math import isfinite
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
import pandas as pd
import re
import warnings
from Turkish_Preprocessing.utils_ import import_corpora, import_mwe_list, import_abbreviations
from Turkish_Preprocessing.modules.normalization import Normalization
import numpy as np
import sys

class Tokenizer():

    def __init__(self):
        self.corpus = import_corpora()
        self.abbr_list = import_abbreviations()
        self.dataset = self.create_dataset()
        self.MWETokenizer = Normalization().MWE_Normalization

    # Rule Based Tokenizer

    def RuleBasedTokenizer(self, text):

        #Rule 1: Put white-space around unambiguous punctuation (? ( ) ; etc.)
        text = re.sub(r"([\?\!\:\)\(\|\;\~\"\"\]\[]+)", r" \1 ", text)
        # # Rule 2: Put white-space around commas that aren’t inside numbers
        text = re.sub(r"(?!^\d)(\,)(?!^\d)", r" \1", text)
        # # Rule 3: Put white-space after single quotes not preceded by a letter
        text = re.sub (r'(\')[^\w+]', r" \1 ", text)
        # # Rule 4: Put white-space after clitics not followed by a letter
        # text = re.sub()
        # Rule 5: For each period, if it is not preceeded by an abbreviation, put white-space before the period
        text = re.sub("".join(map(lambda abbr: f"(?<!{abbr[:-1]})", self.abbr_list))+"(\.)\s", r" \1 ", text)
        # MWE tokenizer
        text = self.MWETokenizer(text)

        tokens = text.split(" ")

        return tokens

    def LogisticTokenizer(self, test):
        """
        Hello
        
        """
        X =  list(self.dataset[:, :self.dataset.shape[1]-1])
        y =  list(self.dataset[:, self.dataset.shape[1]-1])

        clf = LogisticRegression().fit(X,y)
        tagged = clf.predict(self.translate(test))

        tokens = []
        idx = 0
        token = ""
        for t, ch in zip(list(tagged), list(test)):
            if t == 0:
                token += ch

            elif len(token) > 0:
                token += ch
                tokens.append(token)
                token = ""
            else:
                tokens.append(ch)

        tokens.append(token)

        return [token.strip().strip(".").strip(",") for token in tokens if token != " "]

    def create_dataset(self):
    
        # https://aclanthology.org/A00-1012.pdf --> Look at the paper
        
        train_data = []

        for idx, token in enumerate(self.corpus):

            for i, char in enumerate(list(token)):
                
                features = {
                    "is_capital": 0, # Followed by capitalized letter
                    "prev_space": 0, # preceeded by space
                    "forw_space": 0, # Followed by space
                    "is_number": 0, # Followed by space
                    "is_punct": 0, # Is it preceeded by one char before punct or not 
                    "forw_punct": 0, # Is it preceeded by one char before punct or not 
                    "is_acroynm": 0,
                    "class": 0, # how long the previous token before a punct or space
                }

                if char.isupper():
                    features["is_capital"] = 1
                if not char.isalnum() and char in [".",",","\"","\'",]:
                    features["is_punct"] = 1
                try:
                    if not token[i+1].isalnum() and token[i+1] in [".",",","\"","\'"]:
                        features["forw_punct"] = 1
                    
                    elif char[i+1].isnumeric():
                        features["is_number"] = 1
                except:
                    pass
                
                if not len(self.corpus) == idx+1:
                    if not self.corpus[idx+1].isalnum():
                        if not self.corpus[idx+1].isalnum() and not self.corpus[idx+1] in [".",",","\"","\'"]:
                                features["forw_space"] = 1
                        else:
                            features["forw_punct"] = 1

                if i==0 and not char in [".",","]:
                    features["prev_space"] = 1

                if i == len(token)-1:
                    if len(self.corpus) -1 > idx:
                        if not self.corpus[idx+1] in [".",","]:
                            features["forw_space"] = 1
                    if not char.isalnum():
                        if token in self.abbr_list:
                            features["is_acroynm"] = 1
                    features["class"] = 1

                train_data.append(np.array(list(features.values())))

        return np.array(train_data)

    def translate(self, sample):

        test = []
        for idx, char in enumerate(list(sample)):

            features = {
                "is_capital": 0, # Followed by capitalized letter
                "prev_space": 0, # preceeded by space
                "forw_space": 0, # Followed by space
                "is_number": 0, # Followed by space
                "is_punct": 0, # Is it preceeded by one char before punct or not 
                "forw_punct": 0, # Is it preceeded by one char before punct or not 
                "is_acroynm": 0,
            }

            if char.isupper():
                features["is_capital"] = 1
            if not char.isalnum() and char in [".",",","\"","\'",]:
                features["is_punct"] = 1
            try:
                if not char[idx+1].isalnum() and not char[idx+1] == " ":
                    features["forw_punct"] = 1
                elif not char[idx+1].isnumeric():
                    features["is_number"] = 1
            except:
                pass
            
            if not len(sample) == idx+1:
                if not sample[idx+1].isalnum():
                    if sample[idx+1] == " ":
                        features["forw_space"] = 1
                    if sample[idx+1] in [".",",","\"","\'",]:
                        features["forw_punct"] = 1

            if sample[idx-1] == " ":
                features["prev_space"] = 1

            if not char.isalnum():
                sub = ""
                for c in range(idx, 0,-1):
                    if sample[c] == " ":
                        break
                    else:
                        sub = sample[c] + sub
                if sub in self.abbr_list:
                    features["is_acroynm"] = 1

            test.append(np.array(list(features.values())))

        return test