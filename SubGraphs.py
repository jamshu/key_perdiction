from Bio import Medline 
from nltk.corpus import stopwords
import nltk
import networkx as nx
import matplotlib.pyplot as plt
import itertools

from nltk.util import ngrams

stop = stopwords.words('english')

with open("C:\\Users\\Omar\\Documents\\GitHub\\ICLAssignment\\pubmed_result.txt") as handle:
    records = Medline.parse(handle)
    
    for record in records:
        g=nx.Graph()
        recordNoStop = ' '
        for wrd in record["AB"].split():
            if wrd not in stop:recordNoStop  = recordNoStop + wrd + ' '
            
        words=nltk.tokenize.word_tokenize(recordNoStop)
        g.add_nodes_from(words)
        bg=ngrams(words,2)
        g.add_edges_from(bg)

plt.figure()
nx.draw(g,with_labels=True,node_size=3000,font_size=8,font_color="navy",node_color="orange")
plt.show()    


nx.google_matrix(g,alpha=0.85,nodelist=None)

print(nx.google_matrix(g,alpha=0.85,nodelist=None))

#for sub_node in g.nodes():
#   target = nx.ego_graph(g,sub_node)
    #print target.edges()
#    plt.figure()
#    nx.draw(target,with_labels=True,node_size=3000,font_size=8,font_color="navy",node_color="orange")
    
target = g
target = nx.complete_graph(3)
for sub_nodes in itertools.combinations(g.nodes(),len(target.nodes())):
    subg = g.subgraph(sub_nodes)
    if nx.is_connected(subg):
        print subg.edges()
        plt.figure()
        nx.draw(subg,with_labels=True,node_size=3000,font_size=8,font_color="navy",node_color="orange")
        plt.show()
plt.show()
        
#print(nx.shortest_path(g))

        #print(nltk.pos_tag(words))

        ##nx.draw(g,with_labels=True,node_size=3000,font_size=8,font_color="navy",node_color="orange")
        ##plt.show()

        #recordNoStop = ' '
        #for wrd in record["AB"].split():
            #if wrd not in stop:recordNoStop  = recordNoStop + wrd + ' '
        #print(recordNoStop)

        #print(record["AB"])
        #print(record["OT"])



 

#print(txt)
    #words=nltk.tokenize.word_tokenize(txt)
    #print(nltk.pos_tag(words))
    #g=nx.Graph()
    #g.add_nodes_from(words)
    #bg=ngrams(words,2)
    #g.add_edges_from(bg)
    #print("Words as nodes: \n",g.nodes())
    #print("Edges between bigrams: \n", g.edges())
