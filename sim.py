import sys
import math
import random

vectors = sys.argv[1]
gloves = {row[0]:([float(val) for val in row[1:]]) for row in ([line.split() for line in open(vectors).read().strip().split("\n")])}

# random generation, should probably be hardcoded.
codes = [x.lower() for x in open(sys.argv[2]).read().strip().split("\n")]
words = random.sample(codes, 25)
shuffler = [1,1,1,1,1,1,1,1,1,
            -3, -3, -3, -3, -3, -3, -3, -3,
            -10,
            -1, -1, -1, -1, -1, -1, -1]
random.shuffle(shuffler)
roles = {words[i]:shuffler[i] for i in xrange(len(words))}
expected = []

def regen(w=None, r=None):
    global words, roles    
    if w is None:
        words = random.sample(codes, 25)
    else:
        words = w
    if s is None:        
        random.shuffle(shuffler)
        r = shuffler
    roles = {words[i]:r[i] for i in xrange(len(words))}


def mag(vec):
    # returns magnitude, probably a math builtin exists for this
    return math.sqrt(sum([i**2 for i in vec]))

def cosSim(word1, word2):
    # safely returns cosine similarity
    if word1 not in gloves or word2 not in gloves:
        return 0
    vec1 = gloves[word1]
    vec2 = gloves[word2]
    num = sum([vec1[i]*vec2[i] for i in xrange(len(vec1))])
    denom = mag(vec1) * mag(vec2)
    return num/denom

def cut(simScore):
    # reduces noise of unassociated words
    thres = 0.2
    if simScore < thres and simScore > -1*thres:
        return 0
    else:
        return simScore

def scoreWord(word1):
    # returns a list of associated words to word1 from the `good side` 
    wordscores = [(roles[word2], cut(cosSim(word1, word2)), word2) for word2 in roles.keys()]
    sorted_scores = sorted(wordscores, key=lambda x: x[1])
    sorted_scores.reverse()
    for x in xrange(len(wordscores)):
        if (sorted_scores[x][0] < 0 or sorted_scores[x][1] == 0) and x > 0:
            return sorted_scores[:x]
        elif sorted_scores[x][0] < 0:
            return []
    return []


def findWords():
    # for each number, returns the best list of words of that length
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

def pickBest(bests):
    global expected
    # picks the best length of list
    # bests cannot be empty
    bestScore = 0
    bestList = []
    for wordList in bests.items():
        if wordList[1][1] > bestScore:
            bestScore = wordList[1][1]
            bestList = wordList
    print (bestList[1][0], bestList[0])
    expected = bestList[1][2]
