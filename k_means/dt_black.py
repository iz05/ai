import matplotlib.pyplot as plt
import random
from math import log2
import sys, csv

# Tree stuff

from math import log2
import sys, csv

DATA = []
HEADERS = []
CATEGORIES = {}
POSSIBLE_OUTPUTS = set()
LAST_INDEX = -1

def read_data():
    global DATA, HEADERS, CATEGORIES, LAST_INDEX, POSSIBLE_OUTPUTS
    file_name = sys.argv[1]
    file = open(file_name)
    csvreader = csv.reader(file)
    HEADERS = next(csvreader)
    LAST_INDEX = len(HEADERS) - 1
    for i in range(0, LAST_INDEX):
        CATEGORIES[i] = set()

    for row in csvreader:
        if "?" not in row:
            DATA.append(row)
            for i in range(0, LAST_INDEX):
                CATEGORIES[i].add(row[i])
            POSSIBLE_OUTPUTS.add(row[LAST_INDEX])

def selective_entropy(data, category):
    s = 0
    total = len(data)
    if(total == 0):
        return 0
    for thing in CATEGORIES[category]:
        new_data = [d for d in data if d[category] == thing]
        size = len(new_data)
        e = total_entropy(new_data)
        s += e * size / total
    return s

def total_entropy(data):
    dict = {}
    for output in POSSIBLE_OUTPUTS:
        dict[output] = 0
    for d in data:
        output = d[LAST_INDEX]
        dict[output] += 1
    total = len(data)
    if total == 0:
        return 0
    s = 0
    for output in dict:
        num = dict[output] / total
        if num != 0:
            s += -1 * num * log2(num)
    return s

def make_tree(cat, data):
    if(len(data) == 0):
        print("Error: no data.")
    total = total_entropy(data)
    if total == 0: # base case
        return data[0][LAST_INDEX]
    l = sorted([(c, selective_entropy(data, c)) for c in cat], key = lambda x : x[1])
    c, e = l[0] # category that reduces entropy the most
    tree = {}
    nc = cat.copy()
    nc.remove(c)
    for thing in CATEGORIES[c]:
        new_data = [d for d in data if d[c] == thing]
        if(len(new_data) > 0):
            tree[(thing, c)] = make_tree(nc, new_data)
    return tree

def helper_output(f, tree, num):
    keys = sorted(list(tree.keys()))
    category_num = keys[0][1]
    f.write("\t" * num + "* " + HEADERS[category_num] + "?\n")
    for key in keys:
        f.write("\t" * (num + 1) + "* " + key[0])
        if(type(tree[key]) == str):
            f.write(" --> " + tree[key] + "\n")
        else:
            f.write("\n")
            helper_output(f, tree[key], num + 2)

def output(tree):
    f = open('treeout.txt', 'w')
    helper_output(f, tree, 0)
    f.close()

def get_mode(data):
    max_key = None
    for key in data:
        if max_key is None or data[key] > data[max_key]:
            max_key = key
    return max_key

def get_result(tree, data):
    pointer = tree
    while(type(pointer) != str):
        flag = False
        for result, cat in pointer:
            if data[cat] == result:
                flag = True
                pointer = pointer[(result, cat)]
                break
        if not flag:
            key = random.sample(pointer.keys(), 1) # choose a random branch otherwise
            pointer = pointer[key[0]]
    return pointer

read_data()
print(len(DATA))
random.shuffle(DATA)
test_size = int(sys.argv[2])
TEST = DATA[len(DATA) - test_size : ]
DATA = DATA[ : len(DATA) - test_size]
min_size = int(sys.argv[3])
max_size = int(sys.argv[4])
step = int(sys.argv[5])
step = 1
success_rates = []
success_rates_random_forest = []
for size in range(min_size, max_size + step, step):
    # normal tree
    indices = random.sample([i for i in range(0, len(DATA))], size)
    results = set()
    for index in indices:
        results.add(DATA[index][LAST_INDEX])
    tree = make_tree([i for i in range(0, len(CATEGORIES))], [DATA[i] for i in indices])
    success = 0
    for data in TEST:
        predicted_result = get_result(tree, data)
        if predicted_result == data[LAST_INDEX]:
            success += 1
    success_rates.append((size, success / len(TEST)))

    # random forest
    trees = []
    for i in range(0, 10):
        indices = random.sample([i for i in range(0, len(DATA))], size // 10)
        results = set()
        for index in indices:
            results.add(DATA[index][LAST_INDEX])
        tree = make_tree([i for i in range(0, len(CATEGORIES))], [DATA[i] for i in indices])
        trees.append(tree)
    success = 0
    for data in TEST:
        result_forest = {}
        for tree in trees:
            predicted_result = get_result(tree, data)
            if predicted_result not in result_forest:
                result_forest[predicted_result] = 0
            result_forest[predicted_result] += 1
        mode = get_mode(result_forest)
        if mode == data[LAST_INDEX]:
            success += 1
    success_rates_random_forest.append((size, success / len(TEST)))

x_data = [data[0] for data in success_rates]
y_data = [data[1] for data in success_rates]
plt.plot(x_data, y_data, 'ro', label="Normal")
x_data_random = [data[0] for data in success_rates_random_forest]
y_data_random = [data[1] for data in success_rates_random_forest]
plt.plot(x_data_random, y_data_random, 'bo', label = "Random forest classifiers")
plt.legend(loc="upper left")
plt.show()