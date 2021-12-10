# -*- coding: utf-8 -*-

import re
import json
from Turkish_Preprocessing.utils_ import import_corpora
from collections import OrderedDict

###################
#     STEMMER
###################

class Stemmer():

    def __init__(self):
        self.morphology = self.get_morphology()
        self.corpus = import_corpora()

    def get_stem(self, token):
        """
        Verbal
        bild-im
        kalem-im
        [mod (-DIR)
        person - number
        TAM II [idi, imiş, ise, ken)
        TAM I (-DI, -mIş, -Iyor, -(y)AcAk, -Ar/Ir, -sA, -mAlI, -(y)A, -mAktA)
        Modality (-(y)Abil, -(y)Adur, -(y)Abil)
        neg (-mA)
        voice (-Il, -DIr, -In, -Iş)]

        benim kitabım[dt][iıuü]r$

        Nominal
        """
        # Try it with layers !!
        self.morphology = self.get_morphology()

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

    def get_morphology(self):
        return OrderedDict(json.loads(open("Turkish_Preprocessing/source/morphology.json","r").read()))
    
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