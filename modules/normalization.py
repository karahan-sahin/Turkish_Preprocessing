import re
from typing import Text
import warnings
from Turkish_Preprocessing.utils_ import *

################
# NORMALIZATION
################

class Normalization():
    """
    Implicitly defining equivalence classes of terms
    
    U.S.A, USA, US -> USA
    lowercase, lower-case, lower case -> lower-case
    anti-discriminatory, antidiscriminatory -> antidiscriminatory

    # \w+\-\n\w+ --> \w+\w+

    """

    # https://uu.diva-portal.org/smash/get/diva2:1213513/FULLTEXT01.pdf --> Look at the paper

    def __init__(self):
        self.abbr_dict = import_abbreviations()
        self.lexicon = import_norm_lexicon()
        self.mwe_list = import_mwe_list()
        self.proper_nouns = import_proper_nouns()

    ## Rule-Based Normalization

    def normalize(self,text):
        """
        
        """
        text = self.normalize_abbreviation(text)
        text = self.adapt_newline(text)
        text = self.normalize_urls(text)
        text = self.normalize_emails(text)
        text = self.normalize_hashtags(text)
        text = self.remove_punctuation(text)
        text = self.MWE_Normalization(text)
        
        return text

    # def custom_lowercase(self, text):
        
    #     def lower_nonprop(token):
    #         term = token.group(0)
    #         if term not in self.proper_nouns:
    #             term = term.lower()
    #         return term
        
    #     return re.sub("[A-Za-zÇİğüş]+", lower_nonprop, text)

    def normalize_abbreviation(self, text):

        def open_abbr(token):
            token = token.group(1)
            if token in self.abbr_dict.keys():
                token = self.abbr_dict[token]

            return token + " "

        return re.sub("([A-Za-zÇİğüş]+\.)\s", open_abbr, text)

    def approximate_lexicon(self, text):

        def edit_distance(token):
            token = token.group(1)
            for error, norm in self.lexicon:
                if error == token:
                    token = norm

            return token + " "

        return re.sub("([A-Za-zÇİğüş]+\.)\s", edit_distance, text)

    def normalize_urls(self,text):
        return re.sub(r"(http(s)*\:\/\/)+(www\.)*([a-z0-9]+)+(\.[a-z]+)+(/[^\s]+)+(/)*","<URL>",text)

    def normalize_emails(self,text):
        return re.sub(r"[A-Za-z\d\.\_\-]+@([a-z]+\.)*([a-z]+)","<EMAIL>",text)

    def normalize_hashtags(self,text):
        return re.sub(r"#[A-Za-z\d\_]+","<HASHTAG>",text)

    def remove_punctuation(self,text):
        """
        need (.)??
        """
        return re.sub(r",|!|\"|\"|\'|\'", "", text) 

    def remove_accent(self,text):
        return re.sub()

    def adapt_newline(self,text):
        text = re.sub("-\n","",text)
        text = re.sub("\n"," ",text)
        return text

    def MWE_Normalization(self, text):
        try:
            assert self.mwe_list != [], warnings.warn("IMPORT MWE LIST")
            assert self.abbr_list != [], warnings.warn("IMPORT ABBR LIST")
        except:
            pass

        for mwe in self.mwe_list:
            _match = re.findall("".join(map(lambda token: f"{token}[a-zşçığü]*\s", mwe)).strip("\s")+"(?<![\.,\s])", text)
            if _match:
                text = re.sub("".join(map(lambda token: f"{token}[a-zşçığü]*\s", mwe)).strip("\s")+"(?<![\.,\s])", f"{mwe[0]}_{mwe[1]}", text)
                text = re.sub(r"\[td\]", "t", text)
                text = re.sub(r"\[kğ\]", "t", text)

        return text