import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression

table = pd.read_csv('/content/dataset (1).csv')
X = np.array([np.array(table.loc[i,['valute_sign_count','com_words_part','picture_count']]) for i in range(len(table))])
y = np.array([np.array(table.loc[i,['class']]) for i in range(len(table))])
clf =  LogisticRegression(random_state= 0 ).fit( X,  y)
table = pd.read_csv('/content/test_dataset.csv')
X_test = np.array([np.array(table.loc[i,['valute_sign_count','com_words_part','picture_count']]) for i in range(len(table))])
y_test = np.array([np.array(table.loc[i,['class']]) for i in range(len(table))])
clf.score(X_test,y_test)