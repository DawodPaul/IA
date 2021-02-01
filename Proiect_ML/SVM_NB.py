import pandas as pd
import main as m
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import naive_bayes, svm




Corpus = pd.read_csv("train.csv")
Test = pd.read_csv('test.csv')


Corpus['text']= [m.word_proccessing(entry) for entry in Corpus['text']]
Test['text']= [m.word_proccessing(entry) for entry in Test['text']]


Train_X=Corpus['text']
Train_Y=Corpus['label']
Test_X=Test['text']


Encoder = LabelEncoder()
Train_Y = Encoder.fit_transform(Train_Y)


Tfidf_vect = TfidfVectorizer(max_features=2000)
Tfidf_vect.fit(Corpus['text'])


Train_X_Tfidf = Tfidf_vect.transform(Train_X)
Test_X_Tfidf = Tfidf_vect.transform(Test_X)


Naive = naive_bayes.MultinomialNB()
Naive.fit(Train_X_Tfidf,Train_Y)
predictions_NB = Naive.predict(Test_X_Tfidf)


SVM = svm.SVC(C=1.0, kernel='linear',probability=True,decision_function_shape='ovr')
SVM.fit(Train_X_Tfidf,Train_Y)
predictions_SVM = SVM.predict(Test_X_Tfidf)






