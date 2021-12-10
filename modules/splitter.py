import re
from numpy.lib.shape_base import split
import pandas as pd
from Turkish_Preprocessing.utils_ import import_abbreviations, import_corpora

from Turkish_Preprocessing.modules.models.naive_bayes import NaiveBayesClassifier


####################
# SENTENCE SPLITTER
####################
counter = 0

class SentenceSplitter():

    def __init__(self):
        self.corpus = import_corpora(type="splitter")
        self.abbr_list = import_abbreviations()
        self.dataset = self.create_dataset()


    ## Rule-Based Splitter

    def RuleBasedSplitter(self, text):
        """
        </end> ---> not a split
        <end> ---> split
        
        """
        sentences = []

        # Dont split if it is in the abbrevation list
        text = re.sub("("+"".join(map(lambda abbr: f"{abbr[:-1]}|", self.abbr_list)).strip("|")+")\.", r"\1.</end>", text)
        # Do not split if punct
        text = re.sub(r"(\w+\.)(</end>)*?([^\s])", r"\1</end>\3", text)
        # 1.2 -> number prev
        text = re.sub(r"(\d+\.)(\d+)", r"\1</end>\2", text)
        # Don't split if punctuation is within paranthesis
        text = re.sub("([\"\'].+?)(\.)(.+?[\"\'])", r"\1\2</end> \3", text)
        # Only split from end the Multi-punctuation
        text = re.sub(r"(\.|\!|\?)(\.|\!)", r"\1</end>\2", text)
        # Don't end the punctuation such as (1909-?)
        text = re.sub(r"(\?)(\))", r"\1</end>\2", text)
        # Get the rest of the punctuation end of token
        text = re.sub("(\.!?)(?!</end>)", r"\1<end>", text)

        print(text)

        text = re.sub(r"\<\/end\>", "", text)

        return text.split("<end>")


    ## Machine Learning Based Splitter

    def NaiveBayesSplitter(self,test_data):
        
        clf = NaiveBayesClassifier()
        clf.fit(self.dataset[self.dataset.columns[:-1]], self.dataset["class"])

        ids = {}
        def idify(token):
            
            token = token.group(0)
            global counter
            ids[counter] = token
            counter +=1

            return f"<{counter}>"
        
        test_data = re.sub("\.", idify, test_data)
        test_data = re.sub("\n", "\\n", test_data)

        preds = []
        for i in range(1,counter+1):
            punct_env = [match for match in re.findall(".{0,10}<"+str(i)+">.{0,10}",test_data)][0]
            punct_env = re.sub("<"+str(i)+">", ".", punct_env)
            punct_env = re.sub("<\d+>", "!", punct_env)
            idx = "_".join(punct_env.split()).index(".")
            instance = create_test_instance(punct_env, idx)

            preds.append(clf.predict(instance))

        for i in range(1,counter):
            if preds[i-1] == 1:
                test_data = re.sub("<"+str(i)+">", ids[i-1]+"<end>", test_data)
            else:
                test_data = re.sub("<"+str(i)+">", ids[i-1], test_data)

        split = re.split("<end>", test_data)

        return split

    def create_dataset(self):

        # https://aclanthology.org/A00-1012.pdf --> Look at the paper
        
        train_data = []

        for idx, t in enumerate(self.corpus):

            features = {
                "is_capital": 0, # Followed by capitalized letter
                "is_space": 0, # Followed by space
                "is_number": 0, # Preceed by number
                "is_punct": 0, # Is it preceeded by one char before punct or not 
                "is_acroynm": 0,
                "length_prev": 0, # how long the previous token before a punct or space
                "class": 0, # how long the previous token before a punct or space
            }
         
            if t: 

                token = t[0]

                if len(t) == 2:
                    try:
                        if self.corpus[idx+1][0][0].isupper():
                            features["is_capital"] = 1
                    except:
                        features["is_capital"] = 1 

                    features["is_space"] = 1

                    features["is_number"] = 0

                    features["is_punct"] = 0

                    prev_token = self.corpus[idx-1][0]

                    abbr_list = import_abbreviations()
                    if prev_token in abbr_list:
                        features["is_acroynm"] = 1 
                    
                    features["length_prev"] = len(prev_token)
                    
                    features["class"] = 1
                    
                    train_data.append(pd.Series(features))
                
                elif "." in token:
                    
                    indices = [m.span()[0] for m in re.finditer("\.", token)]

                    for p_idx in indices:
                        
                        try:
                            if token[p_idx+1].isupper():
                                features["is_capital"] = 1
                            else:
                                features["is_capital"] = 0

                        except:
                            if self.corpus[idx+1][0][0].isupper():
                                features["is_capital"] = 1
                            else:
                                features["is_capital"] = 0

                        if p_idx == len(token)-1: 
                            features["is_space"] = 1
                        else:
                            features["is_space"] = 0

                        if token[p_idx-1].isnumeric():
                            features["is_number"] = 1
                            if len(token) < p_idx+1:
                                if token[p_idx+1].isnumeric():
                                    features["is_number"] = 1
                        else:
                            features["is_number"] = 0

                        if token[p_idx-1].isalpha() and not token[p_idx-2].isalpha():
                            features["is_punct"] = 1 
                        else:
                            features["is_punct"] = 0

                        abbr_list = import_abbreviations()
                        if token in abbr_list:
                            features["is_acroynm"] = 1 
                        else:
                            features["is_acroynm"] = 0
                        
                        features["length_prev"] = len(token)

                        features["class"] = 0

                        train_data.append(pd.Series(features))

        return pd.DataFrame(train_data)

def create_test_instance(punct_env="", idx=10 ,type="test") -> pd.Series:
    
        features = {
            "is_capital": 0, # Followed by capitalized letter
            "is_space": 0, # Followed by space
            "is_number": 0, # Preceed by number
            "is_punct": 0, # Is it preceeded by one char before punct or not 
            "is_acroynm": 0,
            "length_prev": 0, # how long the previous token before a punct or space
        }

        if re.match(r"^\.\s*([A-Z])", punct_env[idx:]):
            features["is_capital"] = 1

        if re.match("^\.(\s+)", punct_env[idx:]):  
            features["is_space"] = 1

        if re.match("^(\d+)*\.(\d+)|(\d+)*\.(\d+)", punct_env): # How to detect space 
            features["is_number"] = 1

        if re.findall("\.(.{0,1})", punct_env[idx:])[0].isalpha():
            features["is_punct"] = 1

        try:
            prev_token = re.findall(r"(^|[^a-zA-Z0-9şçığ])([a-zA-Z0-9şçığ\-]+\.)$",punct_env[:idx+1])[0][1]

            abbr_list = import_abbreviations()
            if prev_token in abbr_list:
                features["is_acroynm"] = 1 

            features["length_prev"] = len(prev_token.strip(".")) 

        except:
            features["is_punct"] = 1

        return pd.Series(features)