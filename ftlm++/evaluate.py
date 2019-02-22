import json
result = []
with open("submission/dream.tsv", "r") as f:
    l = f.readline()
    l = f.readline()
    while l:
        x, y = l.strip().split()
        x, y = int(x), int(y)
        result += [y]
        l = f.readline()
with open("data/test.json", "r") as f:
    data = json.load(f)
    debug = []
    k = 0
    acc, all = 0, 0
    for i in range(len(data)):
        for j in range(len(data[i][1])):
            all += 1
            if data[i][1][j]["choice"][result[k]] == data[i][1][j]["answer"]:
                acc += 1
            k += 1
    print("accuracy = ", float(acc)/all)
