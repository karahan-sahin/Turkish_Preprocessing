import json
from collections import OrderedDict

def get_morphology():
        return OrderedDict(json.loads(open("Turkish_Preprocessing/source/morphology/morphology.json","r").read()))

def import_norm_lexicon():
    """
    """
    return [norm.strip("\n").split('\t') for norm in open('Turkish_Preprocessing/source/normalization/normalization.txt','r',encoding='utf-8').readlines()]

def import_mwe_list():
    """
    """
    return [mwe.strip("\n").split(' ') for mwe in open('Turkish_Preprocessing/source/normalization/mwe_list_updated.txt','r',encoding='utf-8').readlines()]

def import_abbreviations():
    """

    source: https://www.tdk.gov.tr/icerik/yazim-kurallari/kisaltmalar-dizini/
    
    """
    abbrevations = {}
    for line in open("Turkish_Preprocessing/source/normalization/abbr.txt", 'r', encoding='utf-8').read().split('\n'):
        abbr, norm = line.split('\t')
        abbrevations[abbr] = norm
    return abbrevations

def import_corpora(type="tokenizer", data="train"):
    """
    
    type=tokenizer
    type=splitter
    type=stopwords
    """
    if data == "train":
        c_file = open('Turkish_Preprocessing/source/datasets/train.txt','r',encoding='utf-8').readlines()
        c_file.extend(open('Turkish_Preprocessing/source/datasets/dev.txt','r',encoding='utf-8').readlines())
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
            c_file.extend(open('Turkish_Preprocessing/source/datasets/test.txt','r',encoding='utf-8').readlines())
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
    else:
        c_file = open('Turkish_Preprocessing/source/datasets/test.txt','r',encoding='utf-8').readlines()
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

        elif type == "splitter":
            for token in c_file:
                corpus.append([t.strip('\n') for t in token.split("\t")])

    return corpus

