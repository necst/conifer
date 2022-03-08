from sklearn import tree
import re
import numpy as np


def isLeaf(src_str):
    r = re.match("[0-9]+ \[label=\"", src_str)
    s = re.search("\\\\n", src_str)
    if (r != None and s == None):
        return True
    else:
        return False


def printClassName(src_str, dt_file):
    r = re.search("[0-9]+ \[label=\"", src_str)
    s = re.search("\"\] ;", src_str)
    t = re.search("\\\\n", src_str)
    if (r != None and s != None and t == None):
        print(src_str[r.end():s.start()], end="", file=dt_file)


def printCondition(src_str, dt_file):
    r = re.search("[0-9]+ \[label=\"", src_str)
    s = re.search("\\\\n", src_str)
    if (r != None and s != None):
        print(src_str[r.end():s.start()], end="", file=dt_file)


def getNodeNum(src_str):
    r = re.match("[0-9]+", src_str)
    if (r != None):
        return int(r.group(0))
    else:
        return ""


def getNextLineIndex(src_list, node_num):
    tmp = []
    i = len(src_list) - 1
    for line in reversed(src_list):
        if (getNodeNum(line) == int(node_num)):
            return i
        i -= 1
    return -1


def isNodeInfo(src_str):
    if (re.match('[0-9]+ -> [0-9]+[ ]+;', src_str) != None):
        return True
    else:
        return False


def oppOperator(src_str):
    src_str = src_str.replace("<=", ">")
    src_str = src_str.replace(">=", "<")
    return src_str


def formatTree(line, indent, dt_file, eol):
    # Init to zeros, will store n_nodes and n_leaves
    size = np.array([0, 0])
    # If the first line is just node connection info line, skip it
    if (isNodeInfo(line[0])):
        line = line[1:]

    # Add this node
    size[0] += 1

    # If the first line is a leaf, print its name with \n, otherwise only \n
    if (isLeaf(line[0])):
        print(": ", end="", file=dt_file)
        printClassName(line[0], dt_file)
        print("", file=dt_file, end=eol+'\n')
        return np.array([1, 1])
    else:
        print("", file=dt_file, end=eol+'\n')

    nIndex = getNodeNum(line[0])  # Get node index
    splitIndex = getNextLineIndex(line[1:], nIndex)  # Get split index

    if (len(line[1:splitIndex]) > 0):
        # Print original condition
        print("|   " * indent, end="", file=dt_file)
        printCondition(line[0], dt_file)
        size += formatTree(line[1:splitIndex], indent + 1, dt_file, eol)  # Call recursively for the first part of original tree

    if (len(line[splitIndex - 1:]) > 0):
        # Print opposite condition
        print("|   " * indent, end="", file=dt_file)
        printCondition(oppOperator(line[0]), dt_file)
        size += formatTree(line[splitIndex - 1:], indent + 1, dt_file, eol)  # Call recursively for the second part of original tree

    return size


def printTree(dot_tree, dt_file, eol):
    new_tree = []

    # Preprocess the tree
    for line in dot_tree.split("\n"):
        r = re.search("[0-9]+\\\\n\[([0-9]+[,]?[ ]?)+\]\\\\n", line)
        s = re.search("\[labeldistance=[0-9]+\.?[0-9]*, labelangle=-?[0-9]+, headlabel=\"(False|True)\"\]", line)
        if (r != None):
            line = line[:r.start()] + line[r.end():]
        if (s != None):
            line = line[:s.start()] + line[s.end():]
        new_tree.append(line)

    # Print in Weka format
    n_nodes, n_leaves = formatTree(new_tree[3:-1], 0, dt_file, eol)

    print('\nNumber of Leaves  : \t', n_leaves, file=dt_file, end=eol+'\n')
    print('\nSize of the Tree : \t', n_nodes, file=dt_file, end=eol+'\n')


def generateDecisionTree(clf, feature_cols, classes, fout, eol):
    dot_tree = tree.export_graphviz(clf, out_file=None, class_names=[str(i) for i in classes], label="none", impurity=False,
                                    feature_names=feature_cols)

    printTree(dot_tree, fout, eol)
