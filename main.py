from Bio import Medline
from nltk.corpus import stopwords
from nltk.corpus import treebank
import nltk
import networkx as nx
import matplotlib.pyplot as plt
import xlwt

import operator

from nltk.util import ngrams



def add_sheet(book, name):
    """
    Add a sheet with one line of data
    """
    value = "This sheet is named: %s" % name
    sheet = book.add_sheet(name)
    sheet.write(0,0, value)


def add_styled_sheet(book, name):
    """
    Add a sheet with styles
    """
    value = "This is a styled sheet!"
    sheet = book.add_sheet(name)
    style = 'pattern: pattern solid, fore_colour blue;'
    sheet.row(0).write(0, value, xlwt.Style.easyxf(style))

def writeToExcel(P,R,F,tCount):
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

    book.save("ICLFinal.xls")


# tokenize the abstrat

stop = stopwords.words('english')
#this array to save the none noune and adjective word
tagged_word =[]
SentanceDict = {}
WordSentanceDict = {}
TaggedSentance=[]
recordNoStop = ' '

pTotal=0
rTotal=0
fTotal=0
tCountTotal=0

i=0

for word, tag in treebank.tagged_words():
    if tag == "NN" or tag=="NNP" or tag=="NNS" or tag=="JJ":
        if word !='The' and word !='the':
            tagged_word.append(word)
    #print(word,tag)

#with open("C://t//result_o.txt") as handle:
with open("data.txt") as handle:

    records = Medline.parse(handle)
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    #wordTokenizer = nltk.data.load("")

    for record in records:
        pubmedId = record['PMID']
        abstract = record['AB']
        authorKeywords = record['OT']
        abstractSentances = tokenizer.tokenize(abstract)
        abstractWords =  nltk.tokenize.word_tokenize(abstract)
        print("The PMID",pubmedId)

        print("The Abstract",abstract)
        print("The OT",authorKeywords)
        for sent in abstractSentances:
            SentanceDict[i] = sent
            i = i+1

        for wordToken in abstractWords:
            #count the total number of words in all abstracts
            tCountTotal=tCountTotal+1

            if not(WordSentanceDict.has_key(wordToken)):
                for sent in SentanceDict:
                    if(SentanceDict[sent].find(wordToken)>-1):
                        if(WordSentanceDict.has_key(wordToken)):
                            WordSentanceDict[wordToken].append(SentanceDict[sent])
                        else:
                            WordSentanceDict[wordToken]=[SentanceDict[sent]]

            #removing stop words

            for wrd in abstractWords:
                if ((wrd not in stop) and (wrd in tagged_word)):
                    recordNoStop = recordNoStop + wrd + ' '

            words=nltk.tokenize.word_tokenize(recordNoStop)

        #remove punctuation

        puncString = ".,?!()0123456789"
        for c in words:
            if ((c in puncString) or (c=='.') or (c==',')): words.remove(c)

        #Graph
        g=nx.DiGraph()
        g.add_nodes_from(words)

        #print('Number of keywords in abstract: ',g.number_of_nodes())
        numberOfKeywords = g.number_of_nodes()/3

        bg=ngrams(words,2)
        g.add_edges_from(bg)
        #print("g.edges(data=True)",g.edges(data=True))
        #plt.figure()
        #nx.draw(g,with_labels=True,node_size=3000,font_size=8,font_color="navy",node_color="orange")
        #plt.show()
        #print(g.edges())

        #find all pair in the sentances
        pairEd=""
        pairEdCountDict={}
        maxPairCount=0


        #Begin loop 1
        for item in g.edges():
            pairItem1=0
            pairItemsCount=0

            #begin loop 2
            for sent in abstractSentances:
                pairItem1=0
                pairIndex1=sent.find(item[0])
                pairIndex2=sent.find(item[1])
                if pairIndex1>-1:
                    pairItem1=1
                if pairIndex2>-1 and pairIndex2>pairIndex1 and pairItem1==1:
                    pairItemsCount=pairItemsCount+1
            #End loop 2

            if maxPairCount<pairItemsCount: maxPairCount=pairItemsCount
            pairEdCountDict[item]=pairItemsCount
        #End loop 1


        #print("Pair Count before devision",pairEdCountDict.values())
        #calculate the weight for each edge

        for item in pairEdCountDict:
            pairEdCountDict[item]=pairEdCountDict[item]/(maxPairCount*1.0)


        #print("Max Number of Count",maxPairCount)

        #print("Pair Count after devision",pairEdCountDict.values())


        for u,v,d in g.edges(data=True):
            pairEdge = u + ' ' + v
            pairEdCountDict.get(pairEdge)
            if pairEdCountDict[item]>0:
                d['weight']=pairEdCountDict[item]
            else:
                d['weight']=0.1


        #print("g.edges(data=True)",g.edges(data=True))

        pr = nx.pagerank(g, alpha=0.85, personalization=None,max_iter=100, tol=1.0e-6, nstart=None, weight='weight',dangling=None)
        #print(pr)


        sorted_x = sorted(pr.items(), key=operator.itemgetter(1))

        #print(sorted_x)
        idx = 0
        topKeywords=[]
        for rkw in reversed(sorted_x):
            topKeywords.append(rkw)
            idx=idx+1
            if idx==numberOfKeywords:break

        #print('Top Keywords Below:')
        #for xx in topKeywords:
         #   print(xx)

        #bigrams = nltk.bigrams(abstractWords)
        topKeywordsList = []
        for xx in topKeywords:
            topKeywordsList.append(xx[0])
            # print(xx)
        #---------------------------------------------------
        # Collapce
        # keep the stop words, skip if AND OF




        #bigrams = nltk.bigrams(abstractWords)

        keywordBigram = []
        #print("keywords", topKeywordsList)

        beforeWord=''
        currWord=''
        tempWord=''
        specialStopKeyword=False
        for abswd in abstractWords:

            if specialStopKeyword and abswd in topKeywordsList:
                specialStopKeyword=False
                topKeywordsList.append(currWord+' '+abswd)
                topKeywordsList.remove(beforeWord)
                topKeywordsList.remove(abswd)
                beforeWord = ''
                currWord = ''
                tempWord = ''
            else:
                specialStopKeyword = False
                beforeWord = ''
                currWord = ''
                afterWord = ''
            if (abswd=='of' or abswd=='and') and tempWord!='':
                if tempWord in topKeywordsList:
                    beforeWord=tempWord
                    currWord=beforeWord+' '+abswd
                    specialStopKeyword=True
            if tempWord!='' and tempWord in topKeywordsList and abswd in topKeywordsList:
                topKeywordsList.append(tempWord + ' ' + abswd)
                topKeywordsList.remove(tempWord)
                topKeywordsList.remove(abswd)

            tempWord=abswd


        print("Final Keywords", topKeywordsList)

        # print(list(bigrams))
        # keywordBigram[key[0]]=pair[0]+" "+pair[1]

        #print("Keyword bigram", keywordBigram)
        #---------------------------------------------------

        #print('authorKeywords:')
        #print(authorKeywords)

        TP=0
        FN=0
        FP=0
        print('Checking TP:')
        for key in topKeywordsList:
            if key[0] in authorKeywords:
                TP=TP+1
            if key[0] not in authorKeywords:
                FP=FP+1

        for kw in authorKeywords:
            for key in topKeywordsList:
                if kw != key[0]:
                    FN=FN+1
                    break
        TP=TP*1.0
        FP=FP*1.0
        FN=FN*1.0
        if (TP + FP)!=0:
            P = (TP / (TP + FP)) * 1.0
        else:
            P=0.0
        if (TP + FN)!=0:
            R = (TP / (TP + FN)) * 1.0
        else:
            R=0.0
        if (P + R)!=0:
            F = ((2*R*P)/(P+R)) * 1.0
        else:
            F=0.0
        print('TP=',TP,' FP=',FP,' FN=',FN)
        print('Precision=',P)
        print('Recall=',R)
        print('F-Measure=',F)

        pTotal=pTotal+P
        rTotal=rTotal+R
        fTotal=fTotal+F


writeToExcel(pTotal,rTotal,fTotal,tCountTotal)



        #print(list(bigrams))
