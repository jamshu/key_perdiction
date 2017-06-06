import json
from Bio import Medline
from nltk.corpus import stopwords
from nltk.corpus import treebank
from stoplist import stoplist
from nltk.stem import PorterStemmer
ps = PorterStemmer()
import nltk
import networkx as nx
# import matplotlib.pyplot as plt
import xlwt
from nltk.corpus import stopwords
from pprint import pprint
from copy import copy
import string
import operator
from nltk.util import ngrams
lemma = nltk.wordnet.WordNetLemmatizer()
import re
class DataProcess:
    def __init__(self,path):
        self.path = path
        self.threshold_key_count = 3
    
    def stem_tokens(self,tokens):
        stemList = [lemma.lemmatize(word) for word in tokens]
        tokens = list(set(stemList))
        stems=[x.lower() for x in tokens]
        return stems

    def remove_stop_words(self,tokens):
        for word in stoplist:
            if word in tokens:
                for item in xrange(tokens.count(word)):
                    tokens.remove(word)
        return tokens
    
    def remove_punctuation_string(self,abstract):
        result = re.sub(r"'\s|\`|\-|\;|\*|\(|\<|[|^|.|,|:|?|!|(|)|'|0|1|2|3|4|5|6|7|8|9|<|>|%|+|-|=|/|[|]|~|\*|_|@|>|]|\+|\>|\)", ' ', abstract)
        #abstract = "".join(l for l in abstract if l not in puncString)
        return result
    # def remove_punctuation_striing(self,abstract):
    #     puncString = ".,:?!()'0123456789<>%+-=/[]~*_@"
    #     abstract = "".join(l for l in abstract if l not in puncString)
    #     return abstract
    def check_preprocess_condition(self,record):
        threshold_key_count = self.threshold_key_count
        
        if record.get('OT',[]) and record.get('AB',False) and record.get('PMID',False):
            OT_LIST = record['OT']
            new_ot_list = []
            for ot in OT_LIST:
                remchar = '*/-'
                for rem in remchar:
                    if rem in ot:
                        ot = ot.replace(rem,' ')
                # if len(ot.split()) > 1:
                #     for spl in ot.split():
                #         new_ot_list.append(spl.lower())
                # else:
                new_ot_list.append(ot.lower())
            ab = record['AB']
            ab = self.remove_punctuation_string(ab)
            abstractWords =  nltk.tokenize.word_tokenize(ab)
            words = self.remove_stop_words(abstractWords)
            nouns = self.extract_nouns_adjective(words)
            stemWords = self.stem_tokens(nouns)
            abstract = self.join_words(stemWords)
           
            ot_copy_list = copy(new_ot_list)
            print "ot copy list>>>>>>>>>>>>>>>>>>>",ot_copy_list,OT_LIST
            # for val in ot_copy_list:
            #     if val not in abstractWords:
            #         new_ot_list.remove(val)
            keyword_count = len(new_ot_list)
            if keyword_count <threshold_key_count:
                return False
            print "new ot list>>>>>>>>>>>>>>>>",new_ot_list
            record['OT'] = new_ot_list
            record['tokens'] = stemWords
            record['AB'] = abstract
            return True
        else:
            return False
    def join_words(self,tokens):
        # downcased = [x.lower() for x in tokens]
        joined = " ".join(tokens).encode('utf-8')
        return joined

    def extract_nouns_adjective(self,tokens):
        tagged = nltk.pos_tag(tokens)
        nouns = [word for word,pos in tagged \
            if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS' or pos=="JJ")]
    
        return nouns
    def load_data(self):
        data = []
        with open('data_processed.json') as data_file:    
            data = json.load(data_file)
        return data
    def write_data(self):
        final_list = self.read_data()
        with open('data_processed.json', 'w') as fout:
            json.dump(final_list, fout)
    def read_data(self):
        path = self.path
        final_list = []
        
        with open(path) as handle:
            records = Medline.parse(handle)
            tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
            for record in records:
                new_dict = {}
                check=self.check_preprocess_condition(record)
                if not check:
                    continue
                # abstract = record.get('AB',False)
                # abstractWords =  nltk.tokenize.word_tokenize(abstract)
                # sw = stopwords.words('english')
                # char_to_remove = [',','.','!','?',':']
                # for word in sw:
                #     if word in abstractWords:
                #         abstractWords.remove(word)
                # final_ab = ' '.join(list(abstractWords))
                # #remove punctuations
                # puncString = ".,:?!()0123456789"

                # final_ab = "".join(l for l in final_ab if l not in puncString)

                # final_ab = final_ab.lower()

                # for rmc in puncString:
                #     final_ab=final_ab.replace(rmc,'')
                new_dict['PMID'] = record.get('PMID','')
                new_dict['TI'] = record.get('TI','')
                new_dict['OT'] = record.get('OT',[])
                new_dict['AB'] = record.get('AB','')
                new_dict['tokens'] = record.get('tokens','')
                final_list.append(new_dict)
            print "clean abastract count>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",len(final_list)
            return final_list
