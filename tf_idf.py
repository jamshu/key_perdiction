import pandas as pd
import xlsxwriter
import json
import math
from Bio import Medline
from nltk.corpus import stopwords
from nltk.corpus import treebank
import nltk
# import networkx as nx
# import matplotlib.pyplot as plt
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
import xlrd
class Tfidf:
    def __init__(self,path):
        docList = self.load_data(path)
        self.docList = docList
        # self.wordSet = self.getWordSet()
        # self.wordDictList = self.getWordDictList()
        # self.idfs = self.computeIDF(self.wordDictList)
    
    
    def load_data(self,file_name):
        data = []
        with open('data_processed.json') as data_file:    
            data = json.load(data_file)
        return data
    def temp_to_excel(self):
        res = []
        ot =[]
        for doc in self.docList:
            PMID =  doc.get('PMID','')
            res.append({'PMID':PMID,'PROCESSED_ABSTRACT':doc.get('AB')})
            count =0
            val = {}
            for key in doc.get('OT',[]):
                count+=1
                kw='OT' +str(count)
                val[kw] =key
            val['PMID'] = PMID
            ot.append(val)
        return res,ot
    def temp_top_keys(self):
        workbook =xlrd.open_workbook('processed.xlsx')
        worksheet = workbook.sheet_by_name('top5')
        vals = []
        for x in range(0,499):
            val = {}
            pmid= str(int(worksheet.cell(0,x).value))
            val['pmid'] = pmid
            print "pmid>>>>>>>",pmid 
            keys = []
            for y in range(1,6):
                keys.append(worksheet.cell(y,x).value)
            val['keys'] = keys
            vals.append(val) 
        return vals
    def getWordSet(self):
        docList = self.docList
        dataList = []
        for doc in docList:
            dataList.extend(self.getBagWord(doc))
        return set(dataList)
    # def getWordSet(self):
    #     docList = self.docList
    #     dataList = []
    #     for doc in docList:
    #         abstract =doc.get('AB','')
    #         abstractWords =  nltk.tokenize.word_tokenize(abstract)
    #         dataList.extend(abstractWords)
    #     processData = set(dataList)
    #     stopData = self.remove_stop_words(processData)
    #     stemTokens = self.stem_tokens(stopData)
    #     return stemTokens
    def extract_nouns_adjective(self,tokens):
        tagged = nltk.pos_tag(tokens)
        nouns = [word for word,pos in tagged \
            if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS' or pos=="JJ")]
    
        return nouns


    def stem_tokens(self,tokens):
        stemList = [lemma.lemmatize(word) for word in tokens]
        return list(set(stemList))
    def remove_stop_words(self,tokens):
        for word in stoplist:
            if word in tokens:
                tokens.remove(word)
        return tokens
    def getBagWord(self,doc):
        abstractWords =doc.get('tokens','')

        # abstractWords =  nltk.tokenize.word_tokenize(abstract)
        # stopData = self.remove_stop_words(abstractWords)
        # nouns = self.extract_nouns_adjective(stopData)
        # stemTokens = self.stem_tokens(nouns)
        return list(set(abstractWords))
    def getWordDict(self,bow):
        wordSet = self.getWordSet()
        wordDict = dict.fromkeys(wordSet,0)
        for word in bow:
            wordDict[word] += 1
        del wordSet
        return wordDict
    def getWordDictList(self):
        docList = self.docList
        dataList = []
        for doc in docList:
            bow = self.getBagWord(doc)
            wordDict = self.getWordDict(bow)
            dataList.append(wordDict)
        return dataList



    def computeTF(self,wordDict,bow):
        tfDict = {}
        bowCount  = len(bow)
        for word,count in wordDict.iteritems():
            tfDict[word] = count /float(bowCount)
        return tfDict
    def computeIDF(self,dictList):
        if not dictList:
            return {}
        idfDict = {}
        N = len(dictList)
        idfDict = dict.fromkeys(dictList[0].keys(),0)
        for doc in dictList:
            for word,val in doc.iteritems():
                if val > 0:
                    idfDict[word] += 1
        for word,val in idfDict.iteritems():
            idfDict[word] = math.log(N/float(val))
        return idfDict
    def computeTFIDF(self,tfBow):
        tfidf = {}
        wordDictList = self.getWordDictList()
        idfs = self.computeIDF(wordDictList)
        
        for word,val in tfBow.iteritems():
            tfidf[word] = val * idfs[word]
        return tfidf
    def getTFIDFlist(self):

        docList = self.docList
        dataList = []
        reportList = []
        for doc in docList:
            bow = self.getBagWord(doc)
            wordDict = self.getWordDict(bow)
            tfBow =self.computeTF(wordDict,bow)
            tfidfBow = self.computeTFIDF(tfBow)
            reportList.append(tfidfBow)
            dataList.append({doc['PMID']:tfidfBow})
            del bow,wordDict,tfBow,tfidfBow
        return reportList,dataList
    def getTopKeys(self,k,dictionary):
        return heapq.nlargest(k,dictionary,key=dictionary.get)
    def getOtherKeys(self,dict1,topkeys):
        return list(set(dict1.keys()) - set(topkeys) )
    def getTrueKeys(self,pmid):
        docList = self.docList
        for doc in docList:
            if doc.get('PMID') == pmid:
                return doc.get('OT',[])
        return []
    def getConfusionMatrix(self):
        conf_dict = {'tp':0,'fp':0,'fn':0}
        tp  = fp = fn = 0.0

        docList = self.docList
        data,result = self.getTFIDFlist()
        
        for doc in result:
            for key,value in doc.iteritems():
                pmid = key
                trueKeys = self.getTrueKeys(pmid)
                
                topkeys = self.getTopKeys(5,value)
                # otherkeys = self.getOtherKeys(value,topkeys)
                for top in topkeys:
                    for tk in trueKeys:
                        spk = tk.split(' ')
                        if top in spk:
                            tp +=1
                        if top not in spk:
                            fp +=1
                for ot in trueKeys:
                    spt = ot.split(' ')
                    check_list = []
                    for sp in spt:
                        if sp in topkeys:
                            check_list.append(True)
                        else:
                            check_list.append(False)
                    if not any(check_list):
                        fn +=1
                    
                # tn_list=list(set(otherkeys) - set(trueKeys))
                # tn += len(tn_list)
                
        conf_dict = {'tp':tp,'fp':fp,'fn':fn}
        return conf_dict
    def temp_get_true_keys(self,pmid):
        conf_dict = {'tp':0,'fp':0,'fn':0}
        tp  = fp = fn = 0.0
        docList = self.docList
        res = []
        for doc in docList:
            if doc.get('PMID','') == pmid:
                return doc.get('OT',[])
        return res
    def temp_get_confusion_matrix(self):
        result = self.temp_top_keys()
        docList = self.docList
        tp  = fp = fn = 0.0 
        for doc in result:
            pmid = doc.get('pmid')
            topkeys = doc.get('keys')
            trueKeys = self.temp_get_true_keys(pmid)
            trueKeys_ext = []
            for tk in trueKeys:
                trueKeys_ext.append(tk)
            for top in topkeys:
                if top in trueKeys_ext:
                    tp +=1
                if top not in trueKeys_ext:
                    fp +=1
            for ot in trueKeys:
                if ot not in topkeys:
                    fn +=1
        conf_dict = {'tp':tp,'fp':fp,'fn':fn}
        return conf_dict
    def getPrecision(self):
        # conf_dict = self.getConfusionMatrix()
        conf_dict = self.temp_get_confusion_matrix()
        TP = conf_dict.get('tp',0)
        FP = conf_dict.get('fp',0)
        FN = conf_dict.get('fn',0)
        wordSet = self.getWordSet()
        total_count = len(wordSet)
        del wordSet
        P = F = R =0.0
        if (TP + FP):
            P = (TP / (TP + FP)) 
        
        if (TP + FN):
            R = (TP / (TP + FN)) 
       
        if (P + R):
            F = ((2*R*P)/(P+R)) 
        
        self.writeToExcel(P,R,F,total_count)
        return P,R,F,total_count

    def printReport(self):
            result,dummy = self.getTFIDFlist()
            # from pprint import pprint
            # pprint(result)
            data=pd.DataFrame(result)
            del result,dummy
            writer = pd.ExcelWriter('Tfidf.xlsx', engine='xlsxwriter')
            data.to_excel(writer, sheet_name='Sheet1')
            writer.save()
    def printAbstract(self):
        result,ot = self.temp_to_excel()
        data=pd.DataFrame(result)
        ot_list = pd.DataFrame(ot)

        writer = pd.ExcelWriter('processed_sc.xlsx', engine='xlsxwriter')
        data.to_excel(writer, sheet_name='Document')
        ot_list.to_excel(writer, sheet_name='LIST_OF_OTS')

        writer.save()


        

    def writeToExcel(self,P,R,F,tCount):
        """"""
        book = xlwt.Workbook()
        sheet1 = book.add_sheet("Validation")

        row = sheet1.row(0)
        row.write(0, 'Precision')
        row.write(1, 'Recall')
        row.write(2, 'F-Measure')
        row.write(3, 'Total Number of Words')

        row = sheet1.row(1)
        row.write(0, P)
        row.write(1, R)
        row.write(2, F)
        row.write(3, tCount)

        book.save("Final.xls")
        