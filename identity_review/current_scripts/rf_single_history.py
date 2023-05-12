import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import numpy as np
import os

from sklearn import svm

def create_df(path):
    list_df = []
    list_files = os.listdir(path)

    path_list = [path + item for item in list_files if item != '.DS_Store']
    path_list.sort()
    for item in path_list:
        print(item)
        temp_df = pd.read_csv(item, low_memory=False)
        list_df.append(temp_df)
    final = pd.concat(list_df)
    return final

def create_equal_representation(df):
    malicious = df.loc[df['malicious'] == 1]

    non_mal = df.loc[df['malicious'] == 0]
    non_mal_sample = non_mal.sample(len(malicious))
    print(len(non_mal_sample))

    return pd.concat([malicious, non_mal_sample], ignore_index= True)

path = 'identity_review/csv_output/single_wallet_history/'

df = create_df(path)

need_name = create_equal_representation(df)

X = need_name[['value', 'time_b/w_trans', 'type_of_trans']].to_numpy()
y = [row['malicious'] for index, row in need_name.iterrows()]

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

model = RandomForestClassifier(n_estimators=3, random_state=0)

scores = cross_val_score(model, X, y, cv=10)

print(scores)

# y_pred_test = model.predict(X_test)

# print(accuracy_score(y_test, y_pred_test))

# print(confusion_matrix(y_test, y_pred_test))

# print(classification_report(y_test, y_pred_test))

#cross value test
# is there enough enough varience 
# look at stm
# get total number 
# random sample the non-malicious to get equal sample size, 

# clf = svm.SVC(kernel='linear', C=5).fit(X_train, y_train)
# print(clf.score(X_test, y_test))









