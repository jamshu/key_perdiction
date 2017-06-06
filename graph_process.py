# This file has graph processing class which is doing processed bag words and getting freq and writing to excel
import networkx as nx
import matplotlib.pyplot as plt
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
import re
from collections import Counter


class GraphProcess:
  
    
    def __init__(self,train_count,test_count,train=False):
       #  docList = [{'AB':'Apple has launched the wonderful iphone 7 plus jetblack. the iphone is great. the samsung is wonderful. the iphone battery great. wonderful great samsung amazing iphone. the samsung battery weak. the iphone battery strong.the iphone is one of the most wonderful devices. iphone is the number one competant for samsung. The apple company and samsung company is one of the leading organizations worldwide. Furthermore, there are other organizations that are arising in the field of smart devices. samsung is producing more and more smart devices and competing apple. samsung and apple are forcing nokia to quit the market.','OT':['apple','samsung','company','wonderful','nokia']},
        
       # ]
        # This is the constructor method which take docList from the function  load_data()
        docList = self.load_data() # This Doc List is taking  raw data(which is processed)
        train_count = train_count # Training Count which is an integer field which took the number of data from doc list
        test_count = test_count
        trainDoc =docList[:train_count]
        testDoc =docList[train_count:test_count] # slicing by train count and test count
        self.train = train # this is a bool which check this is training or Test, 
        self.docList = trainDoc
        # self.docList = docList

        self.testDoc = testDoc
    def getSubgraph(self,g,n_count):
        '''
        param g: Graph
        param n_count : n_count usually 3 or 4  which is the number of node in the subgraph

        it take a whole graph and return subgraph with count taking as a parameter
         '''
        subgraph_list =[]
        for sub_nodes in itertools.combinations(g.nodes(),n_count): #iteraing over combination
            subg = g.subgraph(sub_nodes) # current subgraph instance
            if nx.is_connected(subg): #checking this sub graph is connected or not
                edge_list =[] # taking a blank edge list which will fill by sub graph edges
                edges=subg.edges()
                for edge in edges:
                    edge_list.append(set(edge))
                # label = self.get_graph_name(edge_list)
                # subg.label = label
                subgraph_list.append(subg)

        return subgraph_list # returning a sub graph list
      
    def getKeywordKeys(self,vals,label_key_set,vk=False):
        '''
        param vals: 
        param label_key_set:
        param vk:
         '''
        res = set()
        for val in vals:
            bal_keys =label_key_set - set(val.keys())
            bal_dict = dict.fromkeys(bal_keys,0)
            val.update(bal_dict)
            if vk:
                if self.train:
                    val.update({'keyword':1,'non-keyword':0})
            else:
                if self.train:
                    val.update({'keyword':0,'non-keyword':1})
        return True
    def concatKeys(self,keyword_dict,non_keyword_dict):
        kw_keys = set()
        nkw_keys = set()
        for kw_val in keyword_dict:
            kw_keys.update(kw_val.keys())
        for nkw_val in non_keyword_dict:
            nkw_keys.update(nkw_val.keys())

        extra_keys = kw_keys - nkw_keys
        
        for val in keyword_dict:
            bal_keys = extra_keys - set(val.keys())
            bal_dict = dict.fromkeys(bal_keys,0)
            val.update(bal_dict)
        for val in non_keyword_dict:
            bal_keys = extra_keys - set(val.keys())
            bal_dict = dict.fromkeys(bal_keys,0)
            val.update(bal_dict)

    
    # def graphExcel(self,datas):
    #     workbook = xlsxwriter.Workbook('data.xlsx')
    #     worksheet = workbook.add_worksheet()
    #     row = 0
    #     col = 0
    #     for data in datas:
    #         for key in data.keys():
    #             row += 1
    #             worksheet.write(row, col,   key)
    #             for item in data[key]:
    #                 worksheet.write(row, col + 1, item)
    #                 row += 1
    #     workbook.close()
    
    # def graphExcel(self,datas):
    #     workbook = xlsxwriter.Workbook('data.xlsx')
    #     worksheet = workbook.add_worksheet()
    #     row = 0
    #     col = 0
    #     for item in datas:
    #         for col_name, data in item.iteritems():
    #             print "col name>>>> data>>>>>>>",col_name,data
    #             col += 1
    #             worksheet.write(row, col, col_name)
    #             for row_name, row_data in data.iteritems():
    #                 print "row name>>>>>>>>>>> rowdaat>>>>>",row_name,row_data
    #                 col += 1
    #                 row +=1
    #                 worksheet.write(row, col, row_name)
    #                 worksheet.write(row + 1, col, row_data)

    def graphExcel(self,data_dict):
        workbook = xlsxwriter.Workbook('data.xlsx')
        worksheet = workbook.add_worksheet()
        filename = 'GraphProcessTest.xlsx'
        if self.train:
            filename = 'GraphProcessTrain.xlsx'
        writer = pd.ExcelWriter(filename, engine='xlsxwriter')
        frames = []
        for dat in data_dict:
            frames.append(pd.DataFrame.from_dict(dat, orient='index'))
           
        data = pd.concat(frames)
        data.to_excel(writer, sheet_name='Sheet1')
        writer.save()
    def writeToExcel(self):
        keyword_dict,non_keyword_dict = self.docGraph()
        print "keyword dict>>>>>>>>>>>>>>>>>>non keywrd dict",keyword_dict,non_keyword_dict
        self.graphExcel([keyword_dict,non_keyword_dict])
    def docGraph(self):
        keyword_dict = {}
        non_keyword_dict = {}
        label_key_set = set()
        for doc in self.docList:
            g = nx.Graph()
        
            words = self.getBagWord(doc)
            keywords = doc.get('OT',[])
            pmid = doc.get('PMID',False)
            g.add_nodes_from(words)
            bg = ngrams(words,2)
            g.add_edges_from(bg)
            # nx.draw(g,with_labels=True,node_size=3000,font_size=8,font_color="navy",node_color="orange")
            # plt.show()
            print "now generating subgraph>>>>>>>>>>>>>"
            list3 = self.getSubgraph(g,3)
            print "sub graph wihth 3 is completed>>>>>>>>>>>>>>"
            list2 = self.getSubgraph(g,4)
            print "sub graph with 4 is compltedt>>>>>>>>>>>>>>>>>>>>>>>"
            list1 = list2 + list3
            print "compltedte the list"
            print "goint to looop over list1"
            for subg in list1:

                edge_list = []
                nodes = subg.nodes()
                edges = subg.edges()
                for edge in edges:
                    edge_list.append(set(edge))
                for node in nodes:
                    label = self.get_graph_name(node,edge_list)
                    print "label>>>>>>>>>>>>>>>>>>>",label,node
                    # nx.draw(subg,with_labels=True,node_size=3000,font_size=8,font_color="navy",node_color="orange")
                    # plt.show()

                    # possible_label = ['SG121','SG220','SG240',
                    # 'SG123','SG132','SG134','SG231','SG251','SG242','SG262',
                    # 'SG330','SG350','SG370','SG390'
                    # ]
                    # if (label not in possible_label):
                    # if label == 'SG372':

                        # print "not possible label>>>>>>>>>>>>>>>>>>>>>>>>>",label
                        # print "not possible word>>>>>>>>>>>>>>>>>>>>>>>>>>>",node
                        # print "not possible>>>>>edges>>>>>>>>>>>>>>>>>>>>>>>>>>>",edge_list
                        # nx.draw(subg,with_labels=True,node_size=3000,font_size=8,font_color="navy",node_color="orange")
                        # plt.show()
                    label_key_set.add(label)
                
                    if node in keywords:
                        if node in keyword_dict:
                            label_dict =keyword_dict[node]
                            label_val =label_dict.get(label,0) +1
                            label_dict[label] =label_val
                        else:
                            keyword_dict[node] = {label:1,'PMID':pmid}

                    else:
                        if node in non_keyword_dict:
                            label_dict =non_keyword_dict[node]
                            label_val =label_dict.get(label,0) +1
                            label_dict[label] =label_val
                        else:
                            non_keyword_dict[node] = {label:1,'PMID':pmid}
                # print subg.nodes(),keyword_dict
        self.getKeywordKeys(keyword_dict.values(),label_key_set,vk=True)
        self.getKeywordKeys(non_keyword_dict.values(),label_key_set,vk=False)
        # concatKeys(keyword_dict.values(),non_keyword_dict.values())

        return keyword_dict,non_keyword_dict

    

    def get_other_node(self,word,edge):
        # return the other pair of the node in the edge which is not the word
        vals = list(edge)
        for val in vals:
            if val != word:
                return val

    # def get_third_deg(self,word,edges):
    #     print "get third edge >>>>>>>>>>>>> word>>>>>>>>>>>>>>>>>Edges",word,edges
    #     n_list = []
    #     possible_list = []
    #     for edge in edges:
    #         if word not in edge:
    #             n_list.append(edge)
    #     for n_val in n_list:
    #         nv_l = list(n_val)
    #         for val in nv_l:
    #             po_ed = (val,word)
    #             possible_list.append(po_ed)
    #     for pos_val in possible_list:
    #         check_val = set(pos_val)
    #         if check_val in edges:
    #             possible_list.remove(pos_val)
    #     return len(possible_list)
    def get_third_deg(self,word,edges):
        print "get third edge >>>>>>>>>>>>> word>>>>>>>>>>>>>>>>>Edges",word,edges
        n_list = []
        possible_list = []
        other_nodes = set()
        pair_nodes = set()
        for edge in edges:
            nodes = list(edge)
            if word not in edge:
                print "edge>>>>>>>>>>>>>>>>>>>>>",edge
                if nodes and len(nodes) >=1:
                    other_nodes.add(nodes[0]) # Other Node which is the pair in the edge which not the word
                    n_list.append(nodes[0])
                if nodes and len(nodes) >=2:
                    other_nodes.add(nodes[1])
                    n_list.append(nodes[1])
            else:
                if nodes and len(nodes)>=1:
                    pair_nodes.add(nodes[0])
                if nodes and len(nodes)>=2:
                    pair_nodes.add(nodes[1])
        result = other_nodes - pair_nodes
        other_node_list = list(result)
        print "other nodes>>>>>>>>>>>>>>>>>>>>>>>>>>>",other_nodes
        freq_dict = Counter(n_list) # freq dict has the count of repeated words 
        print "freq dict>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",freq_dict
        res =0

        for on in other_node_list: # iterating other node list which are not part of the word
            res+=freq_dict.get(on,0)

        return res # get the third deg 
    def get_graph_name(self,word,edges):

        '''
        It return a graph name
         '''
        if not edges:
            return ''
        
        deg1 = 0 # first degree
        deg2 = 0 # second degree
        deg3 = 0 # third degree
        second_deg_ver =[] # Second deg ver which is easy to find
        for edge in edges: # iterating over edges list
            if word in edge: # if word in edge we increment the deg1
                deg1 +=1
                o_node = self.get_other_node(word,edge) #
                second_deg_ver.append(o_node)
                
        second_ver = list(set(second_deg_ver))
        
        for sec_ver in second_ver:
            for edge in edges:
                if sec_ver in edge:
                    deg2 +=1
        deg3 = self.get_third_deg(word,edges)
        return 'SG' +  str(deg1) + str(deg2) +  str(deg3) # this is the graph name
    def load_data(self):
        # Loading Data from the file data_processed_json,which is used as input of the data in consturctor method
        data = []
        with open('data_processed.json') as data_file:    
            data = json.load(data_file)
        return data
    
    def extract_nouns_adjective(self,tokens):
        tagged = nltk.pos_tag(tokens)
        nouns = [word for word,pos in tagged \
            if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS' or pos=="JJ")]
        return nouns

    def remove_punc(self,abstractWords):
        puncString = ".,:?!()123456789*'^\#@&_<>%+-`=/[]"
        for c in abstractWords:
            if (c in puncString): abstractWords.remove(c)
        return abstractWords


    def remove_punctuation_string(self,abstract):
        puncString = ".,:?!()'0123456789<>%+-=/[]~*_@"
        result = re.sub(r"'\s|\`|\-|\;|\*|\(|\<|[|^|.|,|:|?|!|(|)|'|0|1|2|3|4|5|6|7|8|9|<|>|%|+|-|=|/|[|]|~|\*|_|@|>|]|\+|\>|\)", ' ', abstract)
        #abstract = "".join(l for l in abstract if l not in puncString)
        return result
    def stem_tokens(self,tokens):
        stemList = [lemma.lemmatize(word) for word in tokens]
        return list(set(stemList))
    
    def remove_stop_words(self,tokens):
        for word in stoplist:
            if word in tokens:
                for item in xrange(tokens.count(word)):
                    tokens.remove(word)
        print "tokens after removal>>>>>>>>>>>>>>>>>>>>",tokens
        return tokens
    def lower_words(self,tokens):
        downcased = [x.lower() for x in tokens]
        
        return downcased
    def getBagWord(self,doc):
        abstract =doc.get('AB','')
        abstract = self.remove_punctuation_string(abstract)
        abstractWords =  nltk.tokenize.word_tokenize(abstract)
        abstractWords = self.lower_words(abstractWords)
        # abstractWords = self.remove_punctuation_striing(abstractWords)
        stopData = self.remove_stop_words(abstractWords)
        nouns = self.extract_nouns_adjective(stopData)
        stemTokens = self.stem_tokens(nouns)
        return abstractWords
