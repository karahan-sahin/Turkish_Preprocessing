import json
def import_norm_lexicon():
    """
    """
    return [norm.strip("\n").split('\t') for norm in open('Turkish_Preprocessing/source/normalization.txt','r',encoding='utf-8').readlines()]

def import_proper_nouns():
    """
    """
    return []

def import_mwe_list():
    """
    """
    return [mwe.strip("\n").split(' ') for mwe in open('Turkish_Preprocessing/source/mwe_list_updated.txt','r',encoding='utf-8').readlines()]

# Edit

def import_abbreviations():
    """

    source: https://www.tdk.gov.tr/icerik/yazim-kurallari/kisaltmalar-dizini/
    
    """
    abbrevations = {}
    for line in open("Turkish_Preprocessing/source/abbr.txt", 'r', encoding='utf-8').read().split('\n'):
        abbr, norm = line.split('\t')
        abbrevations[abbr] = norm
    return abbrevations



def import_corpora(type="tokenizer"):
    """
    
    type=tokenizer
    type=splitter
    type=stopwords
    """
    c_file = open('Turkish_Preprocessing/source/train.txt','r',encoding='utf-8').readlines()
    c_file.extend(open('Turkish_Preprocessing/source/dev.txt','r',encoding='utf-8').readlines())
    corpus = []
    if type == "tokenizer":
        doc = []
        for token in c_file:
            if "\t" in token:
                doc.append(token.split("\t")[0].strip('\n'))
                corpus.extend(doc)
                doc = []
            else:
                doc.append(token.strip('\n'))
        
    elif type == "stopwords":
        c_file.extend(open('Turkish_Preprocessing/source/test.txt','r',encoding='utf-8').readlines())
        doc = []
        for token in c_file:
            if "\t" in token:
                doc.append(token.split("\t")[0].strip('\n'))
                corpus.append(doc)
                doc = []
            else:
                doc.append(token.strip('\n'))

    elif type == "splitter":
        for token in c_file:
            corpus.append([t.strip('\n') for t in token.split("\t")])


    return corpus


def LevenstheinDistance(string_1,string_2):
    import numpy as np
    import pandas as pd
    # Not to change the string before the first string
    max_dist = len(string_1) + len(string_2)

    # Matrix with All 0's for edit table
    table = np.zeros((len(string_1)+2, len(string_2)+2),dtype=int)


    # Fill max_dist and Default costs 
    for i in range(0,len(string_1)+2):
        table[i,0] = max_dist
        table[i,1] = i-1

    for j in range(len(string_2)+2):
        table[0,j] = max_dist
        if j != 0:
            table[1,j] = j-1


    # Table values starts at table[2,2]
    for i in range(2,len(string_1)+2):
        for j in range(2,len(string_2)+2):
            #Default --> Replace
            rc = 1
            # If they are the same character
            if string_1[i-2] == string_2[j-2]:
                rc = 0
            # Minimum of operations
            table[i,j] = min(table[i-1,j]+1,    # deletion
                            table[i,j-1]+1,    # insertion
                            table[i-1,j-1]+rc  # replacement/copy
                            )
            # Transposition condition 
            if string_1[i-2] == string_2[j-3] and string_1[i-3] == string_2[j-2]:
                
                table[i,j] = min(table[i,j], table[i-2,j-2] + rc)

    return table[len(string_1)+1, len(string_2)+1]
