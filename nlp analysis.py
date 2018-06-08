# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 15:07:24 2018

@author: herring_j
"""

# Planning text analysis
"""
This is a broken version that performed well due to oversampling before 
train/test split
comments
comments
"""

import nltk
import pandas as pd
import numpy as np
import sklearn
import re
import glob, os, os.path
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.corpus.reader import CategorizedPlaintextCorpusReader
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
from mpl_toolkits.mplot3d import Axes3D
from collections import Counter
from sklearn import decomposition as dc 
from sklearn.model_selection import KFold

data = pd.read_csv('C:\\Users\\herring_j\\Documents\\Projects\\Planning Scraper\\Gas Turbines formatted.csv',encoding = 'latin1')

data = data[['Development Description','Decision','Planning_ref']]

data.shape

data = data.dropna(subset = ['Development Description','Decision'])


data['Decision'].value_counts()

data_sample = data#.sample(500)


'''
Try oversampling smaller class
'''
Refused = data_sample.loc[data_sample['Decision']=='Refused'].sample(1286,replace = True)
data_sample = data_sample.loc[data_sample['Decision']=='Conditional'].append(Refused)

data_sample['Decision'].value_counts()


"""
Create corpus and get BOW representation
"""

mydir = 'C:\\Users\\herring_j\\Documents\\Projects\\Planning Scraper\\Corpus text'
def CreateCorpusFromDataFrame(corpusfolder,df):
    filelist = glob.glob(os.path.join(corpusfolder, "*.txt"))
    for f in filelist:
        try:
            os.remove(f)
        except:
            pass
    corpusfolder
    for index, r in df.iterrows():
        if len(str(r['Development Description']))>0:
            id_=r['Planning_ref']
            body=r['Development Description']
            category=r['Decision']
            fname=str(id_)+'_'+str(category)+'.txt'
            try:
                
                corpusfile=open(corpusfolder+'/'+fname,'a')
                corpusfile.write(str(body))
                corpusfile.close()
                
            except Exception as e:
                print('Error on :'+id_)
                corpusfile.close()
                os.remove(mydir+'\\'+fname)
                pass
        else:
            print('Empty File:'+id)

CreateCorpusFromDataFrame(mydir,data_sample)

my_corpus=CategorizedPlaintextCorpusReader(mydir,r'.*', cat_pattern=r'.*_(.*).txt') 

def preprocess(words, to_lowercase = True, remove_punctuation = True, remove_digits = True, remove_odd_chars = True, remove_stopwords=True, stem = True):
    if to_lowercase:
        words = [w.lower() for w in words]
    
    if remove_punctuation:
        words = [w for w in words if not (re.match(r'^\W+$', w) != None)]
    
    if remove_digits:
        words = [w for w in words if not w.replace('.','',1).isdigit()]

    if remove_odd_chars:
        words = [re.sub(r'[^a-zA-Z0-9_]','_', w) for w in words]
    
    if remove_stopwords:
        sw = set(nltk.corpus.stopwords.words("english"))
        words = [w for w in words if not w in sw]

    if stem:
        porter = nltk.PorterStemmer()
        words = [porter.stem(w) for w in words]
    
    return words

documents = [((fileid, category), preprocess(my_corpus.words(fileid), 
               to_lowercase = True, remove_punctuation = True, remove_digits = True, 
               remove_odd_chars = True, remove_stopwords=True, stem = False)) \
             for category in my_corpus.categories() \
             for fileid in my_corpus.fileids(category)]



def dummy_fun(doc):
    return doc

bow_gen = sklearn.feature_extraction.text.CountVectorizer(
    analyzer='word',
    tokenizer=dummy_fun,
    preprocessor=dummy_fun,
    token_pattern=None,
    ngram_range=(1, 2),
    min_df = 150, # changed from 100
    max_df = 0.85)


bow = bow_gen.fit_transform([doc[1] for doc in documents])
fileids = [doc[0][0] for doc in documents]
print(fileids)
cats = [doc[0][1] for doc in documents]
print(cats)


bow_df = pd.DataFrame(bow.toarray(), columns = bow_gen.get_feature_names())
#bow_df['fileids'] = fileids
#bow_df['target'] = cats
bow_df

dataset = bow_df.copy()





pca = dc.PCA(n_components = 15)
pca.fit(bow_df)
print(pca.explained_variance_ratio_)  

X = pca.transform(bow_df)



colors = {'Conditional':'Green', 'Refused':'Red'}



dataset['target'] = cats


# Plot first 2 PCs
plt.scatter(X[:, 0], X[:, 1],c=dataset['target'].apply(lambda x: colors[x]))


# Plot first 3 PCs
fig = plt.figure(1, figsize=(4, 3))
plt.clf()
ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
ax.scatter(X[:, 0], X[:, 1], X[:, 2],c=dataset['target'].apply(lambda x: colors[x]))


# Logistic regression ----

Y= cats
Y = pd.Series(Y)


X_train, X_test,Y_train,Y_test = sklearn.model_selection.train_test_split(X,Y,train_size = 0.8)



my_model = sklearn.linear_model.LogisticRegression()
my_model.fit(X_train,Y_train)


my_model.score(X_train,Y_train )

predicted = my_model.predict(X_test)
from sklearn import metrics

metrics.accuracy_score(Y_test, predicted)

print(metrics.confusion_matrix(Y_test, predicted))

print(metrics.classification_report(Y_test, predicted))

dataset["target"].value_counts()


# ROC Curve ----

y_score = my_model.decision_function(X_test)




fpr,tpr,thresholds = metrics.roc_curve(Y_test,y_score,pos_label = 'Refused')

roc_auc = metrics.auc(fpr,tpr)

plt.figure()
lw = 2
plt.plot(fpr, tpr, color='darkorange',
         lw=lw, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic')
plt.legend(loc="lower right")
plt.show()


ax2 = plt.gca().twinx()
ax2.set_ylim([np.min(thresholds),2])
ax2.plot(fpr, thresholds, markeredgecolor='r',linestyle='dashed', color='r')
ax2.set_ylabel('Threshold',color='r')



# Cross validation
n = 10
kf = KFold(n_splits=n,shuffle = True)

tr_acc, tr_pre, tr_rec, te_acc, te_pre, te_rec = [],[],[],[],[],[]

tr_conf = np.array([[0,0],[0,0]])
te_conf = np.array([[0,0],[0,0]])


for train_index, test_index in kf.split(X):
    #print("TRAIN:", train_index, "TEST:", test_index)
    X_train_cv, X_test_cv = X[train_index], X[test_index]
    y_train_cv, y_test_cv = Y[train_index], Y[test_index]

    my_model_cv = sklearn.linear_model.LogisticRegression()
    my_model_cv.fit(X_train_cv,y_train_cv)
    
    predicted_cv_tr = my_model_cv.predict(X_train_cv)
    
    tr_pre.append(metrics.precision_score(y_train_cv,predicted_cv_tr,pos_label = 'Refused'))
    tr_rec.append(metrics.recall_score(y_train_cv,predicted_cv_tr,pos_label = 'Refused'))
    tr_acc.append(metrics.accuracy_score(y_train_cv,predicted_cv_tr))
    
    tr_conf = tr_conf + metrics.confusion_matrix(y_train_cv, predicted_cv_tr)
    
    
    predicted_cv_te = my_model_cv.predict(X_test_cv)
    
    te_pre.append(metrics.precision_score(y_test_cv,predicted_cv_te,pos_label = 'Refused'))
    te_rec.append(metrics.recall_score(y_test_cv,predicted_cv_te,pos_label = 'Refused'))
    te_acc.append(metrics.accuracy_score(y_test_cv,predicted_cv_te))
    
    te_conf = te_conf + metrics.confusion_matrix(y_test_cv, predicted_cv_te)

    
te_conf = te_conf/n
tr_conf = tr_conf/n
    

np.mean(tr_pre)
np.mean(te_pre) 
np.mean(tr_acc)
np.mean(te_acc)
np.mean(tr_rec)
np.mean(te_rec) # Must try to improve this

plt.hist(te_rec)











sns.set(style="white")


xx, yy = np.mgrid[-10:10:.01, -10:10:.01]

grid = np.c_[xx.ravel(), yy.ravel()]

probs = my_model.predict_proba(grid)[:, 1].reshape(xx.shape)

f, ax = plt.subplots(figsize=(8, 6))
contour = ax.contourf(xx, yy, probs, 25, cmap="RdBu",
                      vmin=0, vmax=1)
ax_c = f.colorbar(contour)
ax_c.set_label("$P(y = 1)$")
ax_c.set_ticks([0, .25, .5, .75, 1])

ax.scatter(X[:,0],X[:,1], c=dataset['target'].apply(lambda x: colors[x]), s=50,
           cmap="RdBu", vmin=-.2, vmax=1.2,
           edgecolor="white", linewidth=1)


f, ax = plt.subplots(figsize=(8, 6))
ax.contour(xx, yy, probs, levels=[.5], cmap="Greys", vmin=0, vmax=.6)

ax.scatter(X['X1'],X['X2'], c=dataset['target'].apply(lambda x: colors[x]), s=50,
           cmap="RdBu", vmin=-.2, vmax=1.2,
           edgecolor="white", linewidth=1)





"""
Trying TFIDF

"""

tfidf_gen = sklearn.feature_extraction.text.TfidfVectorizer(
    analyzer='word',
    tokenizer=dummy_fun,
    preprocessor=dummy_fun,
    token_pattern=None) 
tfidf = tfidf_gen.fit_transform([doc[1] for doc in documents])
fileids = [doc[0][0] for doc in documents]
cats = [doc[0][1] for doc in documents]
tfidf_df = pd.DataFrame(tfidf.toarray(), columns = tfidf_gen.get_feature_names())
tfidf_df['fileids'] = fileids
tfidf_df['target'] = cats    


dataset = tfidf_df

pca = dc.PCA(n_components = 2)
pca.fit(tfidf_df)
print(pca.explained_variance_ratio_)  

decomposed = pca.transform(tfidf_df)

X = pd.DataFrame({'X1':[i[0] for i in decomposed],'X2':[i[1] for i in decomposed]})


colors = {'Conditional':'Green', 'Refused':'Red'}



dataset['target'] = cats

plt.scatter(X['X1'],X['X2'],c=dataset['target'].apply(lambda x: colors[x]))


# Use X in logistic regression ----











"""
Try word2vec
"""
import os

import nltk
import gensim
import keras 

import matplotlib
import matplotlib.pyplot as plt
import re

import pandas as pd
import numpy as np

import sklearn
import sklearn.naive_bayes
import sklearn.ensemble
import sklearn.datasets
import sklearn.manifold










































