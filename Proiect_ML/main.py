import string
import re
import nltk
import pandas as pd
import numpy as np
import demoji
from sklearn.preprocessing import LabelEncoder
from nltk.corpus import stopwords
from sklearn import naive_bayes,svm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold



def remove_urls (vTEXT):
    vTEXT = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', vTEXT, flags=re.MULTILINE)
    return(vTEXT)

def punctuation(text):
    '''
    Aceasta functie intoarce un text fara nici un o punctuatie, e folosita libraria string
    '''
    for pct in string.punctuation:
        if pct in text:
            t = text.replace(pct," ")
            text = "".join(t)

    return text

def Delete_stopwords_tokenized(text_tokenizat):

    filtered_sentence=[]
    stpw=set(stopwords.words('italian'))
    for cuv in text_tokenizat:
        if cuv not in stpw:
            filtered_sentence.append(cuv)

    return filtered_sentence



def tokenize(text):
    '''Generic wrapper around different tokenization methods.
    '''


    return nltk.TweetTokenizer(preserve_case=False,strip_handles=True).tokenize(text)

def normalize(tokens):
    stemmer= nltk.stem.SnowballStemmer('italian')
    stems=[]
    for token in tokens:
        stems.append(stemmer.stem(token))
    return stems

def demoji_token(token):
    f=[]
    for cuv in token:
        f.append(demoji.replace_with_desc(cuv))

    return f

def word_proccessing(text):
    t = remove_urls(text)
    t = tokenize(t)

    t2 = t
    t = ""
    for word in t2:
        t = t + word + " "



    t = punctuation(t)
    t = tokenize(t)
    t = Delete_stopwords_tokenized(t)
    t = normalize(t)
    t= demoji_token(t)
    return str(t)







def write_prediction(out_file, predictions):
    '''A function to write the predictions to a file.
    id,label
    5001,1
    5002,1
    5003,1
    ...
    '''

    with open(out_file, 'w') as fout:

        fout.write('id,label\n')
        start_id = 5001
        for i, pred in enumerate(predictions):
            linie = str(i + start_id) + ',' + str(pred)  + '\n'
            fout.write(linie)





def split(data, labels, procentaj_valid=0.25):
     return train_test_split(data,labels,test_size=procentaj_valid,shuffle=True)


def cross_validate(k, data,data_label):
    '''Split the data into k chunks.
    iteration 0:
        chunk 0 is for validation, chunk[1:] for train
    iteration 1:
        chunk 1 is for validation, chunk[0] + chunk[2:] for train
    ...
    iteration k:
        chunk k is for validation, chunk[:k] for train
    '''
    kfold = KFold(k,shuffle=False)
    i=1
    cv_svm=np.zeros((2,2))
    cv_nb=np.zeros((2,2))
    for train, test in kfold.split(data,data_label):

        Train_X=data[train]
        Train_Y=data_label[train]
        Test_X=data[test]
        Test_Y=data_label[test]

        Encoder = LabelEncoder()
        Test_Y = Encoder.fit_transform(Test_Y)
        Train_Y = Encoder.fit_transform(Train_Y)

        Tfidf_vect = TfidfVectorizer(max_features=2000)
        Tfidf_vect.fit(data[train])

        Train_X_Tfidf = Tfidf_vect.transform(Train_X)
        Test_X_Tfidf = Tfidf_vect.transform(Test_X)


        Naive = naive_bayes.MultinomialNB()
        Naive.fit(Train_X_Tfidf, Train_Y)
        predictions_NB = Naive.predict(Test_X_Tfidf)
        print("Matrice de confuzie "+str(i)+" NB")
        print(confusion_matrix(Test_Y, predictions_NB))
        cv_nb+=confusion_matrix(Test_Y, predictions_NB)
        SVM = svm.SVC(C=1.0, kernel='linear', probability=True, decision_function_shape='ovr')
        SVM.fit(Train_X_Tfidf, Train_Y)
        predictions_SVM = SVM.predict(Test_X_Tfidf)
        print("Matrice de confuzie " + str(i) + " SVM")
        print(confusion_matrix(Test_Y,predictions_SVM))
        i+=1
        cv_svm+=confusion_matrix(Test_Y,predictions_SVM)
    print(cv_nb)
    print(cv_svm)


train_df = pd.read_csv('train.csv')
test_df = pd.read_csv('test.csv')

cross_validate(10,train_df['text'],train_df['label'])

