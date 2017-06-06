import networkx as nx
# import matplotlib.pyplot as plt
import itertools
import xlsxwriter
import json
import math
from Bio import Medline
from nltk.corpus import stopwords
from nltk.corpus import treebank
import nltk
import xlwt
from nltk.corpus import stopwords
from pprint import pprint
from copy import copy
import string
import operator
from nltk.util import ngrams
lemma = nltk.wordnet.WordNetLemmatizer()
import heapq
from stoplist import stoplist
import pandas as pd

docList = [{'AB':'hello jamshid you fantastic beautiful source code you doing in application,really good work'}]

def get_other_node(word,edge):
    vals = list(edge)
    for val in vals:
        if val != word:
            return val

def get_third_deg(word,edges):
    n_list = []
    possible_list = []
    for edge in edges:
        if word not in edge:
            n_list.append(edge)
    for n_val in n_list:
        nv_l = list(n_val)
        for val in nv_l:
            po_ed = (val,word)
            possible_list.append(po_ed)
    for pos_val in possible_list:
        check_val = set(pos_val)
        if check_val in edges:
            possible_list.remove(pos_val)
    return len(possible_list)
def get_graph_name(word,edges):
        if not edges:
            return ''
        
        deg1 = 0
        deg2 = 0
        deg3 = 0
        second_deg_ver =[]
        for edge in edges:
            if word in edge:
                deg1 +=1
                o_node = get_other_node(word,edge)
                second_deg_ver.append(o_node)
        second_ver = list(set(second_deg_ver))
        # for edge in edges:
        #     if first_node not in edge and (edge[1] or edge[0]) not in second_ver:
        #         deg3 += 1
        for sec_ver in second_ver:
            for edge in edges:
                if sec_ver in edge:
                    deg2 +=1
        deg3 = get_third_deg(word,edges)
        return 'SG' +  str(deg1) + str(deg2) +  str(deg3)


def getSubgraph(g,n_count):
        subgraph_list =[]
        for sub_nodes in itertools.combinations(g.nodes(),n_count):
            subg = g.subgraph(sub_nodes)
            if nx.is_connected(subg):
                edges=subg.edges()
                print "edges>>>>>>>>>>>>>>>>>>>>>>>",edges
                label = get_graph_name(edges)
                subg.label = label
                print "label>>>>>>>>>>>>>>>>>>>",label
                nx.draw(subg,with_labels=True,node_size=3000,font_size=8,font_color="navy",node_color="orange")
                # plt.show()
                subgraph_list.append(subg)
        return subgraph_list
def docGraph():
        keyword_dict = {}
        non_keyword_dict = {}
        label_key_set = set()
        for doc in docList:
            g = nx.Graph()
            words = getBagWord(doc)
           
            g.add_nodes_from(words)
            bg = ngrams(words,2)
            g.add_edges_from(bg)
            list3 = getSubgraph(g,3)
            list2 = []
            list1 = list2 + list3
            for subg in list1:
                label = subg.label
def extract_nouns_adjective(tokens):
        tagged = nltk.pos_tag(tokens)
        nouns = [word for word,pos in tagged \
            if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS' or pos=="JJ")]
        return nouns


def stem_tokens(tokens):
    stemList = [lemma.lemmatize(word) for word in tokens]
    return list(set(stemList))
    
def remove_stop_words(tokens):
    for word in stoplist:
        if word in tokens:
            tokens.remove(word)
    return tokens
    
def getBagWord(doc):
    abstract =doc.get('AB','')
    abstractWords =  nltk.tokenize.word_tokenize(abstract)
    stopData = remove_stop_words(abstractWords)
    nouns = extract_nouns_adjective(stopData)
    stemTokens = stem_tokens(nouns)
    return stemTokens
# docGraph()