# Decision Trees Blue
# Isabella Zhu
# Started 03/31/2022

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

read_data()
tree = make_tree([i for i in range(0, len(CATEGORIES))], DATA)
output(tree)