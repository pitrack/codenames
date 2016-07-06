import sys
import math
import random

vectors = sys.argv[1]
gloves = {row[0]:([float(val) for val in row[1:]]) for row in ([line.split() for line in open(vectors).read().strip().split("\n")])}

# random generation, should probably be hardcoded.
codes = [x.lower() for x in open(sys.argv[2]).read().strip().split("\n")]
words = random.sample(codes, 25)
scores = {word:(2*random.randint(0,2)-3) for word in words}

def mag(vec):
    return math.sqrt(sum([i**2 for i in vec]))

def cosSim(word1, word2):
    if word1 not in gloves or word2 not in gloves:
        return 0
    vec1 = gloves[word1]
    vec2 = gloves[word2]
    num = sum([vec1[i]*vec2[i] for i in xrange(len(vec1))])
    denom = mag(vec1) * mag(vec2)
    return num/denom

def cut(simScore):
    thres = 0.4
    if simScore < thres and simScore > -1*thres:
        return 0
    else:
        return simScore

def scoreWord(word1):
    wordscores = [(scores[word2], cut(cosSim(word1, word2)), word2) for word2 in scores.keys()]
    sorted_scores = sorted(wordscores, key=lambda x: x[1])
    sorted_scores.reverse()
    for x in xrange(len(wordscores)):
        if (sorted_scores[x][0] < 0 or sorted_scores[x][1] == 0) and x > 0:
            return sorted_scores[:x]
        elif sorted_scores[x][0] < 0:
            return []
    return []


def findWord():
    bests = {}
    bestScores = [0] * 25
    for word1 in gloves.keys():
        exp = scoreWord(word1)
        count = len(exp)
        score = sum([x[1] for x in exp])
        if score > bestScores[count]:
            bestScores[count] = score
            bests[count] = (word1, bestScores[count], exp)
    return bests


def regen():
    global words, scores
    words = random.sample(codes, 25)
    scores = {word:(2*random.randint(0,2)-3) for word in words}
