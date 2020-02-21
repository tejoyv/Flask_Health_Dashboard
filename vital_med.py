# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 09:59:50 2020

@author: TEJOY
"""

# Importing the libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Importing the dataset
df = pd.read_csv('vital_med.csv')
df.drop(['Unnamed: 8','Unnamed: 9','Unnamed: 10'],axis=1,inplace=True)
X=df.iloc[:,:-1].values
Y=df.iloc[:,7].values
df

# Describing the dataset
df.isnull().sum()
df.shape
df.describe()

# Create a set of dummy variables from the drugname variable
df = pd.get_dummies(df, columns=['drugname'])

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.25, random_state = 0)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)


# Fitting the Decision Tree to the training set
from sklearn.tree import DecisionTreeClassifier
classifier=DecisionTreeClassifier(criterion='entropy',random_state=0)
classifier.fit(X_train,Y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
cm = confusion_matrix(Y_test, y_pred)
accuracy_score(Y_test, y_pred)

import pickle
pickle.dump(classifier, open(‘model.pkl’, ‘wb’))