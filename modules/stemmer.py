import re
import json
from Turkish_Preprocessing.utils_ import import_corpora, get_morphology

###################
#     STEMMER
###################

class Stemmer():

    def __init__(self):
        self.morphology = get_morphology()

    def get_stem(self, token):

        morph_list = []
        for morph,suffix in self.morphology.items():

            suffix = suffix +"$"

            if re.findall(suffix, token):
                token_sub = re.sub(suffix, "", token)

                if len(token_sub) < 2:
                    pass

                elif self.check_if_consonant(token_sub[-1]) and self.check_if_consonant(token_sub[-2]):
                    pass

                elif (len(token_sub) > 2 or 
                      token_sub == "ol" or
                      token_sub == "et" or
                      token_sub == "su" or
                      token_sub == "in" or
                      token_sub == "bu" or
                      token_sub == "şu" or
                      token_sub == "el" or
                      token_sub == "ev" or
                      token_sub == "al" or
                      token_sub == "at"):

                    token = token_sub
                    morph_list.append(morph)

            if token.endswith("ğ"):
                token = token[:-1] + "k"
        return token, morph_list

    
    
    def check_if_consonant(self,ch):
        if(ch == 'a' or 
           ch == 'e' or 
           ch == 'i' or 
           ch == 'ı' or 
           ch == 'o' or 
           ch == 'u' or
           ch == 'ü'):
            return False
        else:
            return True