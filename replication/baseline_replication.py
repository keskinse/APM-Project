# Copyright (C) 2021  Beate Scheibel
# This file contains code snippets taken out of the edt-ts software.
# For further insight of the whole code, check: https://github.com/bscheibel/edt-ts

import numpy as np
import pandas as pd
import sys
import math
import warnings
import sklearn.exceptions
import re
from sklearn.tree import _tree
from sklearn.tree import DecisionTreeClassifier as tree
from sklearn.tree import export_text
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score
from warnings import simplefilter
warnings.filterwarnings("ignore", category=sklearn.exceptions.UndefinedMetricWarning)
simplefilter(action='ignore', category=FutureWarning)

random_seed = 2
RANDOMSEED = 42

def prepare_dataset(df, id, variable_interest):
    df = df.groupby(id).agg({list, "last"})
    df.columns = [' '.join(col).replace(" ", "") for col in df.columns]
    df[variable_interest + 'list'] = df[variable_interest + 'list'].apply(np.array)
    X = []
    values = df[[variable_interest + 'list']].copy()
    for v in values[variable_interest + 'list']:
        v = v[~np.isnan(v)]
        X.append(v)
    df[variable_interest + 'list'] = X
    df = df.dropna()
    colnames_numerics_only = df.select_dtypes(include=np.number).columns.tolist()
    return df, colnames_numerics_only

def get_rules(model, features, results, result):
    # adapted from: https://mljar.com/blog/extract-rules-decision-tree/
    tree_ = model.tree_
    feature_name = [
        features[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]
    paths = []
    path = []
    def recurse(node, path, paths):
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]
            p1, p2 = list(path), list(path)
            p1 += [f"({name} <= {np.round(threshold, 3)})"]
            recurse(tree_.children_left[node], p1, paths)
            p2 += [f"({name} > {np.round(threshold, 3)})"]
            recurse(tree_.children_right[node], p2, paths)
        else:
            path += [(tree_.value[node], tree_.n_node_samples[node])]
            paths += [path]

    recurse(0, path, paths)
    samples_count = [p[-1][1] for p in paths]
    ii = list(np.argsort(samples_count))
    paths = [paths[i] for i in reversed(ii)]
    rules = []
    for path in paths:
        rule = "IF "
        for p in path[:-1]:
            if rule != "IF ":
                rule += " AND "
            p = re.sub("> 0.5", "== TRUE", p)
            p = re.sub("< 0.5", "== FALSE", p)
            rule += str(p)
        rule += " THEN "
        classes = path[-1][0][0]
        l = np.argmax(classes)
        if results[l] != result:
            continue
        else:
            rule += f"class: {result} "
            rules += [rule]
    return rules

def learn_tree(df, result_column, names, result, results=None, final=False):
    y_var = df[result_column].values
    X_var = df[names]
    features = np.array(list(X_var))
    X_var = X_var[features]
    features = list(X_var)
    X_train, X_test, y_train, y_test = train_test_split(X_var, y_var, test_size=0.20, shuffle=False, stratify=None, random_state=RANDOMSEED)
    clf = tree(random_state=RANDOMSEED)
    model = clf.fit(X_train,y_train)

    pred_model = model.predict(X_test)
    n_nodes = model.tree_.node_count
    max_depth = model.tree_.max_depth
    accuracy = accuracy_score(y_test, pred_model)
    precision = precision_score(y_test, pred_model, average=None)
    used_features = []
    i = 0
    try:
        for f in model.feature_importances_:
            if f > 0:
                used_features.append(features[i])
            i = i + 1
    except:
        pass

    if final:
        text = ""
        text += "Number of nodes total: " + str(n_nodes) + "\n"
        text += 'Accuracy of the model is {:.0%}'.format(accuracy) + "\n"
        text += "Precision: " +  str(precision) + "\n"
        text += "Used features: " + str(used_features) + "\n"
        tree_rules = export_text(model, feature_names=features)
        text += tree_rules + "\n"
        rules = (get_rules(model, features, results, result))
        for r in rules:
            text += r + "\n"
        print(text)
    return accuracy, used_features, text

if __name__ == '__main__' :

    try:
        use_case = sys.argv[1]
    except:
        use_case = "running"

    #preprocessing happens here
    if use_case == "manufacturing":
        file = "data/manufacturing.csv"
        id = "casename"
        results = ['nok', 'ok']
        variable_result = "nok"
        result_column = "case:data_success"
        variable_interest = "data_diameter"
        df = pd.read_csv(file)
        df = df.rename(columns={'sub_concept': 'subname', 'case:concept:name': 'casename'})
        subuuids = dict()
        for index, row in df.iterrows():
            if not math.isnan(row.subname):
                if row.casename in subuuids:
                    if type(subuuids[row.casename]) != list:
                        temp = []
                        temp.append(subuuids[row.casename])
                        temp.append(row.subname)
                        subuuids[row.casename] = temp
                    else:
                        temp = subuuids[row.casename]
                        temp.append(row.subname)
                        subuuids[row.casename] = temp
                else:
                    subuuids[row.casename] = row.subname
        for key, value in subuuids.items():
            subuuids[key] = list(set(value))
        i = 0
        uuids = dict()
        for key, value in subuuids.items():
            for key1, subkeys in subuuids.items():
                for subkey in subkeys:
                    if key == int(subkey):
                        subsub = subuuids[subkey][0]
                        uuids[subkey] = key1
                        uuids[subsub] = key1
                        i = i + 1
        df = df.replace({'casename': uuids})
        df = df.drop(columns="subname")
        df = df.drop(columns="sub_uuid")
        
        df_newFeatures = df[[id, variable_interest]]
        df_newFeatures = df_newFeatures.dropna()
        y_var = df[[id, result_column]].groupby(id).agg('last').dropna().reset_index()
        y_var = y_var[y_var[id].isin(df_newFeatures[id].values)]
        y_var = y_var[result_column].to_numpy()
        df, num_cols = prepare_dataset(df, id, variable_interest)
        df[id] = df.index
        df = df.reset_index(drop=True)
        num_cols.append('casename')
        
    else:
        use_case = "running"
        file = 'data/running.csv'
        id = "uuid"
        results = ['Discard Goods', 'Transfer Goods']
        result_column = 'event'
        variable_result = 'Discard Goods'
        variable_interest = "temperature"
        df = pd.read_csv(file)
        df = df.rename(columns={"timestamp": "time:timestamp"})
        
        df_newFeatures = df.select_dtypes(include=['number'])
        df, num_cols = prepare_dataset(df, id, variable_interest)
        df = df.dropna(axis=1)
        y_var = df[result_column + "last"].to_numpy()
        
    learn_tree(df, result_column + 'last', num_cols, variable_result, results, True)