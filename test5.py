from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer


from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.linear_model import RidgeClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import Perceptron
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.ensemble import RandomForestClassifier
clf = LinearSVC()
vectorizer = CountVectorizer()
corpus = ['This is first document','This is second document',
		'And the third one','Is this the first document?']
test = ['hello','how are you']

X = vectorizer.fit_transform(corpus)
analyze = vectorizer.build_analyzer()
print analyze("This is a text document to analyze.") == (['this', 'is', 'text', 'document', 'to', 'analyze'])
print vectorizer.get_feature_names()
print X.toarray()
print vectorizer.vocabulary_.get('first')
print vectorizer.transform(['Something completely new.']).toarray()
bigram_vectorizer = CountVectorizer(ngram_range=(1, 2),token_pattern=r'\b\w+\b', min_df=1)
print bigram_vectorizer
analyze = bigram_vectorizer.build_analyzer()
print analyze
print analyze('Bi-grams are cool!')
X_2 = bigram_vectorizer.fit_transform(corpus).toarray()
print X_2
feature_index = bigram_vectorizer.vocabulary_.get('is this')
print feature_index
print X_2[:, feature_index]

vectorizer = TfidfVectorizer(min_df=1)
corpus = ['This is first document','This is second document',
		'And the third one','Is this the first document?']
test = ['hello','how are you']
print vectorizer.fit_transform(corpus)
d_train = vectorizer.fit_transform(corpus)
test =vectorizer.fit_transform(test)
clf = LinearSVC()
clf.fit(d_train,test)