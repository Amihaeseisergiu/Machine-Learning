from node import Node
from math import log
import math

def readData(file):
    file1 = open(file, 'r')
    lines = file1.readlines()

    dictionary = {}
    typesDicionary = {}
    headers = lines[0].strip('\n').split(' ')
    types = lines[1].strip('\n').split(' ')
    for i in range(0, len(types)):
        typesDicionary[headers[i]] = types[i]
    for i in headers:
        dictionary[i] = []
    for i in range(2, len(lines)):
        line = lines[i].strip('\n').split(' ')
        for j in range(0, len(headers)):
            dictionary[headers[j]].append(line[j])
    
    return dictionary, typesDicionary

def entropy(data):
    last = list(data.keys())[-1]

    ent = 0
    values = uniqueValues(data[last])

    for val in values:
        fract = data[last].count(val) / len(data[last])
        ent += -fract * math.log(fract, 2)
    return ent

def avgCondEntropy(data, types, attribute):
    last = list(data.keys())[-1]

    exitValues = uniqueValues(data[last])
    attributeValues = uniqueValues(data[attribute])

    if types[attribute] == 'discrete':
        ent2 = 0
        for val in attributeValues:
            ent = 0
            for exitVal in exitValues:
                numi = 0
                num = 0
                for index in range(0, len(data[attribute])):
                    if data[attribute][index] == val and data[last][index] == exitVal:
                        numi += 1
                    if data[attribute][index] == val:
                        num += 1
                fract = numi / num
                if fract != 0:
                    ent += -fract*math.log(fract, 2)
            fract2 = data[attribute].count(val) / len(data[attribute])
            if fract2 != 0:
                ent2 += fract2*ent
        return ent2, None
    else:
        splitValues = []
        valuesSorted = []

        for i in attributeValues:
            valuesSorted.append(float(i))
        valuesSorted.sort()

        for i in range(0, len(valuesSorted) - 1):
            splitValues.append( (float(valuesSorted[i]) + float(valuesSorted[i + 1])) / 2 )

        splitPoint = None
        splitVal = None
        for i in splitValues:
            entLeft = 0
            entRight = 0
            nrElementsLeft = 0
            nrElementsRight = 0
            for j in data[attribute]:
                if float(j) < i:
                    nrElementsLeft += 1
                else:
                    nrElementsRight += 1
            for exitVal in exitValues:
                cont1 = 0
                cont2 = 0
                for index in range(0, len(data[attribute])):
                    if data[last][index] == exitVal and float(data[attribute][index]) < i:
                        cont1 += 1
                    elif data[last][index] == exitVal and float(data[attribute][index]) > i:
                        cont2 += 1
                fract = cont1 / nrElementsLeft
                fract2 = cont2 / nrElementsRight
                if fract != 0:
                    entLeft += -fract*math.log(fract, 2)
                if fract2 != 0:
                    entRight += -fract2*math.log(fract2, 2)
            
            condEnt = (nrElementsLeft / len(data[attribute])) * entLeft + (nrElementsRight / len(data[attribute])) * entRight
            if splitPoint == None:
                splitPoint = i
                splitVal = condEnt
            elif condEnt < splitVal:
                splitPoint = i
                splitVal = condEnt

        return splitVal, splitPoint

def getMaxIG(data, types):
    candidateName = None
    candidateVal = None
    splitPoint = None

    for val in list(data.keys())[:-1]:
        condEnt, sp = avgCondEntropy(data, types, val)
        ent = entropy(data)
        if candidateName == None:
            candidateName = val
            splitPoint = sp
            candidateVal = ent - condEnt
        elif candidateVal < ent - condEnt:
            candidateName = val
            splitPoint = sp
            candidateVal = ent - condEnt
    
    return candidateName, splitPoint

def splitTable(data, node, val):
    ret = {}
    for i in list(data.keys()):
        if i != node:
            ret[i] = []
    
    for i in range(0, len(data[node])):
        if data[node][i] == val:
            for j in list(data.keys()):
                if j != node:
                    ret[j].append(data[j][i])
    return ret

def splitTableCont(data, node, split, direction):
    if direction == 'Left':
        ret = {}
        for i in list(data.keys()):
            ret[i] = []

        for i in range(0, len(data[node])):
            if float(data[node][i]) < split:
                 for j in list(data.keys()):
                    ret[j].append(data[j][i])
        return ret
    else:
        ret = {}
        for i in list(data.keys()):
            ret[i] = []

        for i in range(0, len(data[node])):
            if float(data[node][i]) > split:
                 for j in list(data.keys()):
                    ret[j].append(data[j][i])
        return ret

def uniqueValues(data):
    ret = []
    for i in data:
        if i not in ret:
            ret.append(i)
    return ret

def findCommEl(data):
    max = None
    maxVal = None
    for i in data:
        if max is None:
            max = i
            maxVal = data.count(i)
        elif data.count(i) > maxVal:
            max = i
            maxVal = data.count(i)
    return max

def ID3(data, originalData, features, types, parentNode = None):

    if len(uniqueValues(data[list(data.keys())[-1]])) <= 1:
        return Node(uniqueValues(data[list(data.keys())[-1]])[0], findCommEl(data[list(data.keys())[-1]]))
    elif len(data) == 0:
        return Node(findCommEl(originalData[list(originalData.keys())[-1]]), findCommEl(data[list(data.keys())[-1]]))
    elif len(features) == 0:
        return Node(parentNode, findCommEl(data[list(data.keys())[-1]]))
    else:
        parentNode = findCommEl(originalData[list(originalData.keys())[-1]])

        best_feature, splitPoint = getMaxIG(data, types)
        tree = Node(best_feature, findCommEl(data[list(data.keys())[-1]]))

        if splitPoint == None:
            features = [i for i in features if i != best_feature]

            for value in uniqueValues(data[best_feature]):
                subData = splitTable(data, best_feature, value)

                subtree = ID3(subData, originalData, features, types, parentNode)
                subtree.parent = tree
                subtree.branchValue = value
                tree.children[value] = subtree
        else:
            tree.continuous = True
            tree.splitAttr = splitPoint

            subLeft = splitTableCont(data, best_feature, splitPoint, 'Left')
            subtree = ID3(subLeft, originalData, features, types, parentNode)
            subtree.parent = tree
            subtree.branchValue = '< ' + str(splitPoint)
            tree.children['< ' + str(splitPoint)] = subtree

            subRight = splitTableCont(data, best_feature, splitPoint, 'Right')
            subtree2 = ID3(subRight, originalData, features, types, parentNode)
            subtree2.parent = tree
            subtree2.branchValue = '> ' + str(splitPoint)
            tree.children['> ' + str(splitPoint)] = subtree2

        return tree

def predict(query, types, tree, default = 1):
    if len(tree.children) == 0:
        return tree.label
    for key in list(query.keys()):
        if key == tree.label and ((types[key] == 'continuous' and tree.continuous) or (types[key] == 'discrete' and not tree.continuous)):
            if not tree.pruned:
                if tree.continuous:
                    if float(query[key]) < tree.splitAttr:
                        return predict(query, types, tree.children['< ' + str(tree.splitAttr)])
                    else:
                        return predict(query, types, tree.children['> ' + str(tree.splitAttr)])
                else:
                    for k, v in tree.children.items():
                        if k == query[key]:
                            return predict(query, types, v)
            else:
                return tree.mostCommon
            return default

def accuracy(tree, query, types):
    correct = 0
    attributes = query.copy()
    del attributes[list(attributes.keys())[-1]]
    
    for count in range(0, len(attributes[list(attributes.keys())[0]])):
        validCase = {}
        for key in list(attributes.keys()):
            validCase[key] = attributes[key][count]
        if predict(validCase, types, tree) == query[list(query.keys())[-1]][count]:
            correct += 1
    
    return correct / len(query[list(query.keys())[-1]])

def prune_node(node, val_instances, types):
    if len(node.children) == 0:
        accuracy_before_pruning = accuracy(node, val_instances, types)
        node.pruned = True

        if accuracy_before_pruning >= accuracy(node, val_instances, types):
            node.pruned = False
        return

    for value, child_node in node.children.items():
        prune_node(child_node, val_instances, types)

    accuracy_before_pruning = accuracy(node, val_instances, types)
    node.pruned = True

    if accuracy_before_pruning >= accuracy(node, val_instances, types):
        node.pruned = False

def formatData(t, s):
    first = True
    #print('\t'*s + 'Most common on branch %s'%t.mostCommon)
    if t.pruned:
        print('\t' * s + str(t.mostCommon))
    else:
        for key, value in t.children.items():
            if first:
                if t.continuous:
                    print('\t' * s + "IF " + str(t.label) + " " + str(key) + " THEN")
                else:
                    print('\t' * s + "IF " + str(t.label) + " = " + str(key) + " THEN")
                first = False
            else:
                if t.continuous:
                    print('\t' * s + "ELSE IF " + str(t.label) + " " + str(key) + " THEN")
                else:
                    print('\t' * s + "ELSE IF " + str(t.label) + " = " + str(key) + " THEN")
            if len(value.children) != 0:
                formatData(value, s+1)
            else:
                print('\t' * (s+1) + str(value.label))
                #print('\t'*s + 'Most common on branch %s'%value.mostCommon)

def testTree(query, types, tree):
    for count in range(0, len(query[list(query.keys())[0]])):
        testCase = {}
        for key in list(query.keys()):
            testCase[key] = query[key][count]
        print("Test case %d outcome: %s" % (count, predict(testCase, types, tree)))

train, trainTypes = readData('data/train2.txt')
test, testTypes = readData('data/test2.txt')
validate, validateTypes = readData('data/validate2.txt')
t = ID3(train, train, list(train.keys())[:-1], trainTypes)
formatData(t, 0)
testTree(test, testTypes, t)

prune_node(t, validate, validateTypes)
formatData(t, 0)

trainCont, trainTypesCont = readData('data/train3.txt')
testCont, testTypesCont = readData('data/test3.txt')
tCont = ID3(trainCont, trainCont, list(trainCont.keys())[:-1], trainTypesCont)
formatData(tCont, 0)
testTree(testCont, testTypesCont, tCont)
