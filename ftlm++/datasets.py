import os
import csv
import numpy as np
import json
import nltk

from tqdm import tqdm

from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split

seed = 3535999445

def dream(path):    
    X, Y = [], []
    for i in range(3): #set
        X += [[]]
        Y += [[]]
        for j in range(5):
            X[i] += [[]]

    for k in range(3):
        if k == 2:
            y = 0
        with open(os.path.join(path, ["train.json", "dev.json", "test.json"][k]), "r") as f:
            data = json.load(f)
            for i in range(len(data)):                
                for j in range(len(data[i][1])):
                    q = data[i][1][j]["question"]
                    s = ''
                    
                    speakers = {}
                    speakers['ALL'] = []
                    for it in range(len(data[i][0])):
                        turn = data[i][0][it]
                        speaker = turn.split(":")[0].lower()
                        if speaker not in speakers:
                            speakers[speaker] = []
                        
                    ql = nltk.word_tokenize(q.lower())

                    if 'w' in speakers and (
                                            'woman' in ql or 'girl' in ql or 'her' in ql or 'she' in ql) and 'man' not in ql and 'boy' not in ql and 'he' not in ql and 'his' not in ql:
                        sq = 'w'
                    elif 'm' in speakers and (
                                            'man' in ql or 'boy' in ql or 'his' in ql or 'he' in ql) and 'woman' not in ql and 'girl' not in ql and 'her' not in ql and 'she' not in ql:
                        sq = 'm'
                    elif 'woman' in speakers and (
                                            'woman' in ql or 'girl' in ql or 'her' in ql or 'she' in ql) and 'man' not in ql and 'boy' not in ql and 'he' not in ql and 'his' not in ql:
                        sq = 'woman'
                    elif 'man' in speakers and (
                                            'man' in ql or 'boy' in ql or 'his' in ql or 'he' in ql) and 'woman' not in ql and 'girl' not in ql and 'her' not in ql and 'she' not in ql:
                        sq = 'man'
                    elif 'f' in speakers and (
                                            'woman' in ql or 'girl' in ql or 'her' in ql or 'she' in ql) and 'man' not in ql and 'boy' not in ql and 'he' not in ql and 'his' not in ql:
                        sq = 'f'
                    else:
                        ok = False
                        for speaker in speakers:
                            if speaker in ql:
                                ok = True
                                for s in speakers:
                                    if s != speaker and s in ql:
                                        ok = False
                                if ok:
                                    sq = speaker
                                    break
                        if not ok:
                            sq = 'ALL'
                    for it in range(len(data[i][0])):
                        turn = data[i][0][it]
                        speaker = turn.split(":")[0].lower()
                        if sq == 'ALL' or speaker == sq:
                            s += '[[SQ]]' + turn + '[[/SQ]]'
                        else:
                            s += turn
                            
                    X[k][0] += [s]
                    X[k][1] += [q]
                    for l in range(3):
                        c = data[i][1][j]["choice"][l]
                        X[k][l+2] += [c]
                        if k != 2 and c == data[i][1][j]["answer"]:
                            y = l
                    Y[k] += [y]
    trX1, trX2, trX3, trX4, trX5 = X[0][0], X[0][1], X[0][2], X[0][3], X[0][4]
    vaX1, vaX2, vaX3, vaX4, vaX5 = X[1][0], X[1][1], X[1][2], X[1][3], X[1][4]
    teX1, teX2, teX3, teX4, teX5 = X[2][0], X[2][1], X[2][2], X[2][3], X[2][4]
    trY = np.asarray(Y[0], dtype=np.int32)
    vaY = np.asarray(Y[1], dtype=np.int32)
    teY = np.asarray(Y[2], dtype=np.int32)
    return (trX1, trX2, trX3, trX4, trX5, trY), (vaX1, vaX2, vaX3, vaX4, vaX5, vaY), (teX1, teX2, teX3, teX4, teX5),\
