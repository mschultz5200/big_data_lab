import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import numpy as np
import os

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

path = 'identity_review/csv_output/single_wallet_history/'

df = create_df(path)

X = df[['value', 'time_b/w_trans', 'type_of_trans']].to_numpy()
y = [row['malicious'] for index, row in df.iterrows()]

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1, stratify=y)

model = RandomForestClassifier(n_estimators=3, random_state=0).fit(X_train, y_train)

y_pred_test = model.predict(X_test)

print(accuracy_score(y_test, y_pred_test))

print(confusion_matrix(y_test, y_pred_test))

print(classification_report(y_test, y_pred_test))








