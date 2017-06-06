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
# dt = DataProcess('pubmed_result.txt')
# dt.write_data()
# print "doc list>>>>>>>>>>>>",docList
tf = Tfidf('data_processed.json')
# wordDictList = tf.wordDictList
# print "word Dict list"
# idfs = tf.computeIDF(wordDictList)
# tf.printAbstract()
print "result",tf.getPrecision()
# tf.temp_top_keys()