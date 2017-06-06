from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn .svm import LinearSVC 
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
clf = LinearSVC()
vectorizer = TfidfVectorizer()
train_data = ['hello','you','there','test','dragon','jumbo']
test_data = ['hello','you','there','test','check','job','second','rac']
train_vectors = vectorizer.fit_transform(train_data)
test_vectors = vectorizer.transform(test_data)
print "train vecotros>>>>>>>>>>>>>>>>",train_vectors,test_vectors
clf.fit(train_vectors,test_vectors)
