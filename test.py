from Bio import Medline
from nltk.corpus import stopwords
from nltk.corpus import treebank
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
from data_process import DataProcess 
from tf_idf import Tfidf
# row_line = []
# with open('stoplist.txt') as f:
# 	for line in f.readlines():
# 		row_line.append(line.rstrip())
# print row_line
dt = DataProcess('pubmed_result.txt')
docList = [{'AB':"you just want that computer"},{'AB':"hello namasthe you are beautiful"}]
docList = dt.read_data()
# print "doc list>>>>>>>>>>>>",docList
tf = Tfidf(docList)
# wordDictList = tf.wordDictList
# print "word Dict list"
# idfs = tf.computeIDF(wordDictList)

print "result",tf.getPrecision()
# print "result>>>>>>>>>>>>>>>>>>>>>>>>>>>>",tf.printReport()
# def read_data(self):
#         path = self.path
#         final_list = []
#         with open(path) as handle:
#             records = Medline.parse(handle)
#             tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
#             for record in records:
#                 check=self.check_preprocess_condition(record)
#                 if not check:
#                     continue
#                 abstract = record.get('AB',False)
#                 abstractWords =  nltk.tokenize.word_tokenize(abstract)
#                 sw = stopwords.words('english')
#                 char_to_remove = [',','.','!','?',':']
#                 for word in sw:
#                     if word in abstractWords:
#                         abstractWords.remove(word)
#                 final_ab = ' '.join(list(abstractWords))
#                 #remove punctuations
#                 puncString = ".,:?!()0123456789"

#                 final_ab = "".join(l for l in final_ab if l not in puncString)

#                 final_ab = final_ab.lower()
#                 for rmc in puncString:
#                     final_ab=final_ab.replace(rmc,'')
#                 record['AB'] = final_ab
#                 final_list.append(record)
#             return final_list



# essays = u"""text how are you man,you? are the most beautiful boy in the world"""
# tokens = nltk.word_tokenize(essays)
# tagged = nltk.pos_tag(tokens)
# nouns = [word for word,pos in tagged \
#     if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS' or pos=="JJ")]
# downcased = [x.lower() for x in nouns]
# joined = " ".join(downcased).encode('utf-8')
# into_string = str(nouns)
# print "joined >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",joined

# output = open("output.txt", "w")
# output.write(joined)
# output.close()


# count = 0
# def check_preprocess_condition(record):
#     if record.get('OT',[]) and record.get('AB',False) and record.get('PMID',False):
#         OT_LIST = record['OT']

#         ab = record['AB']
#         abstractWords =  nltk.tokenize.word_tokenize(ab)
#         # print "ab>>>>>>>>>>>>>>>words>>>>>>",abstractWords
#         # print "OT_list>>>>>>>>>>>>>>>>>>>>>>first",OT_LIST,type(OT_LIST)
#         ot_copy_list = copy(OT_LIST)
#         for val in ot_copy_list:
#             # print "val >>>>>>>>>>>>>>>>>>",val.lower()
#             if (val and val.lower()) not in abstractWords:
#                 OT_LIST.remove(val)

#         # print "OT list>>>>>>>>>>>>>",OT_LIST
#         keyword_count = len(OT_LIST)
#         # print "keyword_count>>>>>>>>>>>>>>>>>>>",keyword_count
#         if keyword_count <3:
#             return False
#         record['OT'] = OT_LIST

#         return True
#     else:
#         return False
# with open("data.txt") as handle:
#     records = Medline.parse(handle)
#     tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
#     final_list = []
#     for record in records:
#         print "OT first time",record.get('OT')
#         check=check_preprocess_condition(record)
#         if not check:
#             continue
#         count += 1
#         pubmedId = record.get('PMID',False)
#         abstract = record.get('AB',False)
#         authorKeywords = record.get('OT',[])

#         abstractSentances = tokenizer.tokenize(abstract)
#         abstractWords =  nltk.tokenize.word_tokenize(abstract)
#         sw = stopwords.words('english')
#         char_to_remove = [',','.','!','?',':']

#         for word in sw:
#             if word in abstractWords:
#                 abstractWords.remove(word)

#         final_ab = ' '.join(list(abstractWords))
#         #remove punctuations
#         final_ab = "".join(l for l in final_ab if l not in string.punctuation)
#         #
#         # for rmc in char_to_remove:
#         #     final_ab=final_ab.replace(rmc,'')
#         record['AB'] = final_ab

#         # print "Final OT>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",record['OT']
#         # print "final AB>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",final_ab
#         final_list.append(record)
#         # print "final_list>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",final_list
#         # print("The PMID",pubmedId)
