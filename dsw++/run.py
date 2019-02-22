import json
import nltk
from string import punctuation
from nltk.corpus import stopwords
import math
import numpy as np
import os.path
import gzip
import codecs

def run(fn, test = False):
    U = set(stopwords.words('english'))
    def normtime(ss):
        s = [x for x in ss]
        for i in range(1, len(s) - 1):
            if s[i] in ['past', 'to'] and s[i + 1].isdigit() and (
                    s[i - 1] is not None and s[i - 1].isdigit() or s[i - 1] in ['half', 'quater']):
                if s[i - 1].isdigit():
                    x = int(s[i - 1])
                elif s[i - 1] == 'half':
                    x = 30
                else:  # quater
                    x = 15
                y = int(s[i + 1])
                if s[i] == 'to':
                    x = 60 - x
                    y -= 1
                if x > 0 and x < 60 and y >= 0 and y <= 24:
                    xy = str(y) + ":" + str(x)
                    s[i - 1] = xy
                    s[i] = None
                    s[i + 1] = None
        s = [x for x in s if x is not None]
        return s

    #from https://stackoverflow.com/questions/493174/is-there-a-way-to-convert-number-words-to-integers
    def text2int(textnum, numwords={}):
        if not numwords:
            units = [
                "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
                "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
                "sixteen", "seventeen", "eighteen", "nineteen",
            ]

            tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

            scales = ["hundred", "thousand", "million", "billion", "trillion"]

            numwords["and"] = (1, 0)
            for idx, word in enumerate(units):  numwords[word] = (1, idx)
            for idx, word in enumerate(tens):       numwords[word] = (1, idx * 10)
            for idx, word in enumerate(scales): numwords[word] = (10 ** (idx * 3 or 2), 0)

        ordinal_words = {'first': 1, 'second': 2, 'third': 3, 'fifth': 5, 'eighth': 8, 'ninth': 9, 'twelfth': 12}
        ordinal_endings = [('ieth', 'y'), ('th', '')]

        textnum = textnum.replace('-', ' ')

        current = result = 0
        curstring = ""
        onnumber = False
        for word in textnum.split():
            if word in ordinal_words:
                scale, increment = (1, ordinal_words[word])
                current = current * scale + increment
                if scale > 100:
                    result += current
                    current = 0
                onnumber = True
            else:
                for ending, replacement in ordinal_endings:
                    if word.endswith(ending):
                        word = "%s%s" % (word[:-len(ending)], replacement)

                if word not in numwords:
                    if onnumber:
                        curstring += repr(result + current) + " "
                    curstring += word + " "
                    result = current = 0
                    onnumber = False
                else:
                    scale, increment = numwords[word]

                    current = current * scale + increment
                    if scale > 100:
                        result += current
                        current = 0
                    onnumber = True

        if onnumber:
            curstring += repr(result + current)

        return curstring

    def gt(s):
        s = ''.join([(c if (c==':' or c not in punctuation) else '') for c in s.lower()])
        s = text2int(s)
        s = nltk.word_tokenize(s)
        s = normtime(s)
        return s

    def cossim(u, v):
        uv = np.average(u * v)
        uu = np.average(np.square(u))
        vv = np.average(np.square(v))
        return 0 if not uv.any() else (uv / np.sqrt(uu * vv))

    def get_vector():
        tk = set()
        with open(fn, "r") as f:
            data = json.load(f)
            for i in range(len(data)):
                for j in range(len(data[i][1])):
                    qt = gt(data[i][1][j]["question"])
                    for t in qt:
                        tk.add(t)
                    for k in range(len(data[i][1][j]["choice"])):
                        at = gt(data[i][1][j]["choice"][k])
                        for t in at:
                            tk.add(t)
                ct = gt('\n'.join(data[i][0]))
                for t in ct:
                    tk.add(t)
        token = {}
        with gzip.open("data/numberbatch-en-17.06.txt.gz", "rt", encoding='utf-8') as f:
            l = f.readline()
            l = f.readline()
            while l:
                l = l.strip().split()
                if l[0] in tk:
                    token[l[0]] = l[1:]
                l = f.readline()
        for x in token:
            for i in range(300):
                token[x][i] = float(token[x][i])
        return token

    vector = get_vector()
    for x in vector:
        vector[x] = np.asarray(vector[x])

    def dp(P, SQ, SA):
        d = 100000
        for i in range(len(P)):
            if P[i] in SQ:
                for j in range(i, len(P)):
                    if P[j] in SA:
                        d = min(abs(j-i), d)
                        break
                    if abs(j-i) >= d:
                        break
                for j in range(i, -1, -1):
                    if P[j] in SA:
                        d = min(abs(j-i), d)
                        break
                    if abs(j-i) >= d:
                        break
        return d+1

    if test:
        prediction = []
    else:
        acc = 0
        all = 0
    
    with open(fn, 'r') as f:
        dialog = json.load(f)
        for i in range(0, len(dialog)):
            PW = {}
            P = {}
            C = {}
            IC = {}

            PW['ALL'] = set()
            P['ALL'] = []
            C['ALL'] = {}
            IC['ALL'] = {}

            for it in range(len(dialog[i][0])):
                turn = dialog[i][0][it]
                speaker = turn.split(":")[0].lower()

                if speaker not in PW:
                    PW[speaker] = set()
                    P[speaker] = []
                    C[speaker] = {}
                    IC[speaker] = {}

            for it in range(len(dialog[i][0])):
                turn = dialog[i][0][it]
                speaker = turn.split(":")[0].lower()

                if turn.endswith("?") and it+1 < len(dialog[i][0]):
                    nt = gt(":".join(dialog[i][0][it+1].split(":")[1:]).lower().split(".")[0])
                    if "no" in nt:
                        turn = '.'.join(turn.split(".")[:-1])

                tt = gt(turn)
                for t in tt:
                    if t == 'i':
                        if speaker in ['m', 'man']:
                            t = 'man'
                        elif speaker in ['f', 'w', 'woman']:
                            t = 'woman'

                    PW['ALL'].add(t)
                    P['ALL'] += [t]
                    if t not in C['ALL']:
                        C['ALL'][t] = 0
                    C['ALL'][t] += 1

                    PW[speaker].add(t)
                    P[speaker] += [t]
                    if t not in C[speaker]:
                        C[speaker][t] = 0
                    C[speaker][t] += 1

            for speaker in IC:
                for t in C[speaker]:
                    IC[speaker][t] = math.log(1+1/C[speaker][t])
            for j in range(len(dialog[i][1])):
                ql= gt(dialog[i][1][j]["question"])
                score = []
                Q = set()
                for t in ql:
                    Q.add(t)
                SQ = {}
                for speaker in PW:
                    SQ[speaker] = (Q & PW[speaker]) - U

                if 'w' in PW and (
                                'woman' in ql or 'girl' in ql or 'her' in ql or 'she' in ql) and 'man' not in ql and 'boy' not in ql and 'he' not in ql and 'his' not in ql:
                    sq = 'w'
                elif 'm' in PW and (
                                'man' in ql or 'boy' in ql or 'his' in ql or 'he' in ql) and 'woman' not in ql and 'girl' not in ql and 'her' not in ql and 'she' not in ql:
                    sq = 'm'
                elif 'woman' in PW and (
                                'woman' in ql or 'girl' in ql or 'her' in ql or 'she' in ql) and 'man' not in ql and 'boy' not in ql and 'he' not in ql and 'his' not in ql:
                    sq = 'woman'
                elif 'man' in PW and (
                                'man' in ql or 'boy' in ql or 'his' in ql or 'he' in ql) and 'woman' not in ql and 'girl' not in ql and 'her' not in ql and 'she' not in ql:
                    sq = 'man'
                elif 'f' in PW and (
                                'woman' in ql or 'girl' in ql or 'her' in ql or 'she' in ql) and 'man' not in ql and 'boy' not in ql and 'he' not in ql and 'his' not in ql:
                    sq = 'f'
                else:
                    ok = False
                    for speaker in PW:
                        if speaker in ql:
                            ok = True
                            for s in PW:
                                if s != speaker and s in ql:
                                    ok = False
                            if ok:
                                sq = speaker
                                break
                    if not ok:
                        sq = 'ALL'

                for k in range(len(dialog[i][1][j]["choice"])):
                    A = set()
                    for t in gt(dialog[i][1][j]["choice"][k]):
                        A.add(t)
                    S = A | Q
                    SA = {}
                    swk = {}
                    dk = {}
                    for speaker in PW:
                        SA[speaker] = ((A & PW[speaker]) - Q) - U

                        if len(SQ[speaker]) == 0 or len(SA[speaker]) == 0:
                            dk[speaker] = 1
                        else:
                            dk[speaker] = 1/(len(P[speaker]) - 1) * dp(P[speaker], SQ[speaker], SA[speaker])

                        PIC = [0]
                        for t in P[speaker]:
                            if t in A or t in Q:
                                pic = IC[speaker][t]
                            else:
                                pic = 0
                            PIC += [pic + PIC[-1]]

                        swk[speaker] = -100000
                        for l in range(0, len(P[speaker])):
                            swk[speaker] = max(swk[speaker],(PIC[min(l + len(S), len(P[speaker]))] - PIC[l]))

                    for speaker in PW:
                        swk[speaker] -= dk[speaker]

                    if sq == 'ALL':
                        swk_final = swk[sq]
                    else:
                        swk_final = swk[sq] * 0.5 + swk['ALL'] * 0.5

                    score += [swk_final]

                vecd = {}
                vecd['ALL'] = [np.zeros(300)]
                for turn in dialog[i][0]:
                    speaker = turn.split(":")[0].lower()

                    if speaker not in vecd:
                        vecd[speaker] = [np.zeros(300)]
                    for t in gt(':'.join(turn.split(":")[1:])):
                        if t in vector and t not in U:
                            vecd['ALL'] += [vecd['ALL'][-1] + vector[t]]
                            vecd[speaker] += [vecd[speaker][-1] + vector[t]]

                choice, ce = 0, -100000
                for k in range(len(dialog[i][1][j]["choice"])):
                    v = np.zeros(300)
                    windowsize = 0
                    for t in gt(dialog[i][1][j]["choice"][k]):
                        if t in vector and t not in U:
                            windowsize += 1
                            v += vector[t]

                    ceksq = -1
                    for window in range(len(vecd[sq]) - windowsize):
                        diff = vecd[sq][window + windowsize] - vecd[sq][window]
                        cekw = cossim(v, diff)
                        if cekw > ceksq:
                            ceksq = cekw

                    cekall = -1
                    for window in range(len(vecd['ALL']) - windowsize):
                        diff = vecd['ALL'][window + windowsize] - vecd['ALL'][window]
                        cekw = cossim(v, diff)
                        if cekw > cekall:
                            cekall = cekw

                    cek = ceksq * 0.5 + cekall * 0.5
                    if cek > ce:
                        ce = cek
                        choice = k
                    score[k] += cek

                highest = -100000
                for k in range(len(score)):
                    if score[k] > highest:
                        highest = score[k]
                        choice = k

                if test:
                    prediction += [choice]
                else:
                    if dialog[i][1][j]["choice"][choice] == dialog[i][1][j]["answer"]:
                        acc += 1
                    all += 1

    if test:
        try:
            os.mkdir("submission")
        except:
            pass
        with open("submission/dream.tsv", "w") as f:
            f.write("index\tprediction\n")
            for i in range(len(prediction)):
                f.write(str(i)+"\t"+str(prediction[i])+"\n")
    else:
        print("accuracy on", fn, "=", float(acc)/all)

run("data/train.json")
run("data/dev.json")
run("data/test.json", test=True)
