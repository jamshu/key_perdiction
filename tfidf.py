import pandas as pd
import math
docA = "the cat sat on my face"
docB = "the dog sat on my bed"
#Tokeniztion
bowA = docA.split(" ")
bowB = docB.split(" ")
wordSet=set(bowA).union(set(bowB))
print "word set",wordSet
#dict
wordDictA = dict.fromkeys(wordSet,0)
wordDictB = dict.fromkeys(wordSet,0)

for word in bowA:
    wordDictA[word] += 1

for word in bowB:
    wordDictB[word] += 1
print "WordDictA>>>>>>>>>>>>>>>>>",wordDictA
def computeTF(wordDict,bow):
    tfDict = {}
    bowCount  = len(bow)
    for word,count in wordDict.iteritems():
        tfDict[word] = count /float(bowCount)
    return tfDict

tfBowA = computeTF(wordDictA,bowA)
tfBowB = computeTF(wordDictB,bowB)
print "tfBowA>>>>>>>>>>>>>>>>>>>>",tfBowA
def computeIDF(docList):
    if not docList:
        return {}
    idfDict = {}
    N = len(docList)
    idfDict = dict.fromkeys(docList[0].keys(),0)
    for doc in docList:
        for word,val in doc.iteritems():
            if val > 0:
                idfDict[word] += 1
    for word,val in idfDict.iteritems():
        idfDict[word] = math.log(N/float(val))
    return idfDict

idfs = computeIDF([wordDictA,wordDictB])
print "idfs>>>>>>>>>>>>>>>>>>>>>>>>>>>>",idfs
def computeTFIDF(tfBow,idfs):
    tfidf = {}

    for word,val in tfBow.iteritems():
        tfidf[word] = val * idfs[word]
    return tfidf

tfidfBowA = computeTFIDF(tfBowA,idfs)
tfidfBowB = computeTFIDF(tfBowB,idfs)

data=pd.DataFrame([tfidfBowA,tfidfBowB])
# print data
