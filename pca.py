import sys,os,os.path
import argparse
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import pandas as pd
import mglearn
import numpy as np
import matplotlib.pyplot as plt

from pandas.compat import StringIO, BytesIO

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return open(arg, 'r')  # return an open file hand


def main():    
    parser = argparse.ArgumentParser(
        description='ML for Crush is used to iterrogate data extracted from.')
    
    parser.add_argument('-i', dest="file",required=True,
                        help="Path to data file",
                        metavar="FILE",
                        type=lambda x: is_valid_file(parser,x))
                        
     

    args = parser.parse_args()        
    df = pd.read_csv(args.file.name).replace(np.nan, 0, regex=True) #nrows=30
    target = df[['Gender']]
    features = df.iloc[:,3:]

    X_train,X_test,y_train,y_test=train_test_split(features,target,random_state=0)
    print("X_train shape: {}".format(X_train.shape))
    print("y_train shape: {}".format(y_train.shape))
    print("X_test shape: {}".format(X_test.shape))
    print("y_test shape: {}".format(y_test.shape))


    #pd.plotting.scatter_matrix(features,figsize=(15,15),marker='o',hist_kwds={'bins':20},s=60,alpha=.8,cmap=mglearn.cm3)
    #plt.show()

    from sklearn.neighbors import KNeighborsClassifier
    knn = KNeighborsClassifier(n_neighbors=1)
    knn.fit(X_train,y_train.values.ravel())

    y_pred = knn.predict(X_test)
    #print(y_pred)
    #print(y_test)
    print("Test set predictions:\n {}".format(y_pred))
    print("Test set tests:\n {}".format(y_test))
    #print("test set score: {:.2f}".format(np.mean(y_pred == y_test.values.tolist())))   
    print("test set score: {:.2f}".format(knn.score(X_test,y_test)))

    exit()

if __name__ == '__main__':
    main()

# ###############
# iris_dataset = load_iris()

# print("Keys of iris_dataset: \n{}".format(iris_dataset.keys()))
# print(iris_dataset['DESCR'][:193]+"\n...")
# print("Target names: {}".format(iris_dataset['target_names']))
# print("Feature names: {}".format(iris_dataset['feature_names']))
# print("Type of data: {}".format(type(iris_dataset['data'])))
# print("Shape of data: {}".format(iris_dataset['data'].shape))
# print("First five rows of data: \n{}".format(iris_dataset['data'][:5]))
# print("Type of target: {}".format(type(iris_dataset['target'])))
# print("Shape of target: {}".format(iris_dataset['target']))

# ###

# X_train,X_test,y_train,y_test=train_test_split(iris_dataset['data'],iris_dataset['target'],random_state=0)
# print("X_train shape: {}".format(X_train.shape))
# print("y_train shape: {}".format(y_train.shape))
# print("X_test shape: {}".format(X_test.shape))
# print("y_test shape: {}".format(y_test.shape))

# ###
# iris_dataframe = pd.DataFrame(X_train,columns=iris_dataset.feature_names)
# pd.plotting.scatter_matrix(iris_dataframe,c=y_train,figsize=(15,15),marker='o',hist_kwds={'bins':20},s=60,alpha=.8,cmap=mglearn.cm3)

# plt.show()
# ###
# from sklearn.neighbors import KNeighborsClassifier
# knn = KNeighborsClassifier(n_neighbors=1)
# knn.fit(X_train,y_train)
# #KNeighborsClassifier(algorithm='auto',leaf_size=30,metric='minkowski',metric_params=None,n_jobs=1,n_neighbors=1,p=2,weights='uniform')

# ##Make the predictions
# print("We are going to predict a class of flower by entering four measurements:\n")
# sepal_len = float(input("Enter a sepal length (cm):"))
# sepal_width = float(input("Enter a sepal width (cm):"))
# petal_len = float(input("Enter a petal length (cm):"))
# petal_width=float(input("Enter a petal width (cm):"))
# X_new = np.array([[sepal_len,sepal_width,petal_len,petal_width]])
# #X_new=np.array([[5,2.9,1,0.2],[4,2,2,0.5]])
# print("X_new.shape: {}".format(X_new.shape))

# prediction = knn.predict(X_new)
# print("Prediction: {}".format(prediction))
# print("Predicted target name: {}".format(
#     iris_dataset['target_names'][prediction]
# ))

# y_pred = knn.predict(X_test)
# print("Test set predictions:\n {}".format(y_pred))

# print("test set score: {:.2f}".format(np.mean(y_pred == y_test)))   
# print("test set score: {:.2f}".format(knn.score(X_test,y_test)))