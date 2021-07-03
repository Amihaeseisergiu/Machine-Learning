import math

def entropy(partition):
    result = 0
    base = sum(partition)
    for i in partition:
        if(i != 0):
            result += -i/base * math.log(i/base, 2)
    return result

def program(count, m = 2, n = 2):
    
    if(len(count[0]) != m or len(count) != n):
        print('Invalid input data')
        return

    rootPartition = []
    for i in range(0, m):
        temp = 0
        for j in range(0, n):
            temp += count[j][i]
        rootPartition.append(temp)

    print('Root entropy: %f'%entropy(rootPartition))

    for i in range(0, n):
        print('Specific conditional entropy for node %d: %f' % (i, entropy(count[i])))

    avgConditionalEntropy = 0
    for i in range(0, n):
        avgConditionalEntropy += sum(count[i]) / sum(rootPartition) * entropy(count[i])

    print('Average condition entropy: %f' % avgConditionalEntropy)

    print('Information gain: %f' % (entropy(rootPartition) - avgConditionalEntropy))
    
program([[2, 1, 1], [0, 1, 1]], 3, 2)