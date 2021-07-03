import random
import matplotlib.pyplot as plot
from random import randint
from math import sqrt

def readData(file):
    file1 = open(file, 'r')
    lines = file1.readlines()
    data = []
    dimension = len(list(lines[0].strip('\n').split(',')))

    for i in range(0, len(lines)):
        line = [int(j) for j in lines[i].strip('\n').split(',')]

        if len(line) != dimension:
            raise Exception("Variable dimensions")

        data.append(line)
    
    return data

def euclideanDistance(point1, point2):
    if isinstance(point1, list):
        sumation = 0

        for i in range(len(point1)):
            sumation += (point1[i] - point2[i]) ** 2
        
        return sqrt(sumation)
    else:
        return sqrt((point1 - point2) ** 2)

def getCentroid(cluster):
    centroid = []

    for i in range(len(cluster[0])):
        sumation = 0

        for j in range(len(cluster)):
            sumation += cluster[j][i]

        centroid.append(sumation / len(cluster))

    return centroid

def getClusters(real_data, kernelized_data, clusters):
    real_clusters = [[] for i in range(len(clusters))]

    for i in range(len(clusters)):
        for point in clusters[i]:
            position = 0

            for j in range(len(kernelized_data)):
                if point == kernelized_data[j]:
                    position = j
                    break
            
            real_clusters[i].append(real_data[position])
    
    return real_clusters

def converge(centroids1, centroids2):
    for i in range(len(centroids1)):
        if centroids1[i] != centroids2[i]:
            return False

    return True

def plot2D(centroids, clusters, K, initial = False):

    if len(centroids[0]) == 2:
        for i in range(K):
            color = (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))

            for cluster in clusters[i]:
                plot.scatter(cluster[0], cluster[1], color=color, s=30)
                    
        if not initial:
            for i in range(len(centroids)):
                plot.scatter(centroids[i][0], centroids[i][1], s = 130, marker = "x")

                for cluster in clusters[i]:
                    plot.plot([cluster[0], centroids[i][0]], [cluster[1], centroids[i][1]], ':', color='b', linewidth=1)

            for i in range(len(centroids)):
                for j in range(i + 1, len(centroids)):
                    plot.plot([centroids[i][0], centroids[j][0]], [centroids[i][1], centroids[j][1]], ':', color='black')

                    mx = (centroids[i][0] + centroids[j][0]) / 2
                    my = (centroids[i][1] + centroids[j][1]) / 2
                    dx = centroids[j][0] - centroids[i][0]
                    dy = centroids[j][1] - centroids[i][1]

                    l = sqrt(dx ** 2 + dy ** 2)
                    ux = -dy/l
                    uy = dx/l

                    plot.plot([mx + ux, mx - ux], [my + uy, my - uy], color='black')

        if initial:
            plot.ion()
            plot.show()
            plot.pause(1)
            plot.clf()
        else:
            plot.draw()
            plot.pause(10)
            plot.clf()

def minus(vector1, vector2):
    vector = []

    for i in range(len(vector1)):
        vector.append(vector1[i] - vector2[i])

    return vector

def dot(vector1, vector2):
    result = 0

    for i in range(len(vector1)):
        result += vector1[i] * vector2[i]
    
    return result

def cohesion(data, centroids, clusters):
    result = 0

    for entry in data:
        for i in range(len(clusters)):
            for element in clusters[i]:
                if entry == element:
                    result += dot(minus(entry, centroids[i]), minus(entry, centroids[i]))

    return result

def secondDegreePolynomial(vector1, vector2):
    return (dot(vector1, vector2) + 1) ** 2

def kernel(data):
    Gram = [[0] * len(data) for i in range(len(data))]

    for i in range(len(data)):
        for j in range(i, len(data)):
            if i != j:
                Gram[i][j] = secondDegreePolynomial(data[i], data[j])
                Gram[j][i] = Gram[i][j]
    return Gram

def Kmeans(data, K, initial = None, initial_pos = None, kernelized = False):
    initial_centroids = []
    real_data = data.copy()

    if kernelized:
        data = kernel(real_data)

    if initial != None:
        initial_centroids = initial.copy()
    elif initial_pos != None:
        for pos in initial_pos:
            initial_centroids.append(data[pos])
    else:
        available_points = data.copy()

        for i in range(K):
            r = randint(0, len(available_points) - 1)
            initial_centroids.append(available_points[r])
            del available_points[r]

    plot2D(initial_centroids, [data], 1, True)

    while True:
        clusters = [[] for i in range(K)]
        centroids = []
        
        for i in range(len(data)):
            minimum = euclideanDistance(data[i], initial_centroids[0])

            centroid = 0

            for j in range(len(initial_centroids)):
                distance = euclideanDistance(data[i], initial_centroids[j])

                if distance < minimum:
                    minimum = distance
                    centroid = j
            
            clusters[centroid].append(data[i])

        for i in range(len(clusters)):
            centroids.append(getCentroid(clusters[i]))

        if converge(centroids, initial_centroids):
            if not kernelized:
                return clusters
            else:
                return getClusters(real_data, data, clusters)

        print("Cohesion: %f"%cohesion(data, initial_centroids, clusters))
        plot2D(initial_centroids, clusters, K)

        initial_centroids = centroids.copy()

data = readData('./dataset1.csv')

result = Kmeans(data, 3, [[2,10], [5,8], [1,2]])

print(result)

data = readData('./dataset2.csv')

result = Kmeans(data, 2, [[-1,0], [3,1]])

print(result)

data = readData('./dataset3.csv')

result = Kmeans(data, 2, initial_pos=[0, 1], kernelized=True)

print(result)