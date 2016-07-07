import sys
import math
import random
import numpy as np
import time

beginInit = time.time()
vectors = sys.argv[1]
gloves = {row[0]:(np.array([float(val) for val in row[1:]])) for row in ([line.split() for line in open(vectors).read().strip().split("\n")])}
mags = {word: np.sqrt(np.dot(vec,vec)) for (word, vec) in gloves.items()}

# random generation, should probably be hardcoded.
codes = [x.lower() for x in open(sys.argv[2]).read().strip().split("\n")]
words = random.sample(codes, 25)
shuffler = [1,1,1,1,1,1,1,1,1,
            -3, -3, -3, -3, -3, -3, -3, -3,
            -10,
            -1, -1, -1, -1, -1, -1, -1]
random.shuffle(shuffler)
roles = {words[i]:(shuffler[i], False) for i in xrange(len(words))}
expected = []
endInit = time.time()
initTime = endInit - beginInit
findWordsTime = 0

def regen(w=None, r=None):
    # restart with new words
    global words, roles    
    if w is None:
        words = random.sample(codes, 25)
    else:
        words = w
    if r is None:        
        random.shuffle(shuffler)
        r = shuffler
    roles = {words[i]:(r[i], False) for i in xrange(len(words))}

def cosSim(word1, word2):
    # safely returns cosine similarity
    if word1 not in gloves or word2 not in gloves:
        return 0
    vec1 = gloves[word1]
    vec2 = gloves[word2]
    num = np.dot(vec1, vec2)
    denom = mags[word1]*mags[word2]
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
    wordscores = [(role, cut(cosSim(word1, word2)), word2) 
                  for word2, (role, revealed) in roles.items()
                  if not revealed]
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
    global findWordsTime
    start = time.time()
    bests = {}
    bestScores = [0] * 25
    for word1 in gloves.keys():
        exp = scoreWord(word1)
        count = len(exp)
        score = sum([x[1] for x in exp])
        if score > bestScores[count] and word1 not in words:
            bestScores[count] = score
            bests[count] = (word1, bestScores[count], exp)
    end = time.time()
    findWordsTime = end-start
    return bests

def pickBest(bests):
    # picks the best length of list
    # bests cannot be empty
    global expected
    bestScore = 0
    bestList = []
    for wordList in bests.items():
        if wordList[1][1] > bestScore:
            bestScore = wordList[1][1]
            bestList = wordList
    print (bestList[1][0], bestList[0])
    expected = bestList[1][2]

def guess(word):
    # allows user to guess in single player mode
    global words, roles
    if word not in roles:
        print word + " not found in word list."
    elif roles[word][1]:
        print word + " was already guessed."
    elif roles[word][0] == 1:
        print "Correct!"
    elif roles[word][0] == -1:
        print "Incorrect!, An innocent was uncovered."
    elif roles[word][0] == -3:
        print "Incorrect!, Opposing team gets a point."
    elif roles[word][0] == -10:
        print "Incorrect!, GAME OVER"
    roles[word] = (roles[word][0], True)


def board():
    # pretty print of board
    display = roles.items()
    output = "\t"
    for x in xrange(5):
        for y in xrange(5):
            value = 5*x + y
            wordinfo = display[value]
            if not display[value][1][1]:
                cellString = "{}".format(wordinfo[0])
            else:
                cellString = "{} {}".format(wordinfo[0], wordinfo[1][0])
            output+= "{}{}".format(cellString, " " * (17-len(cellString)))
        output += "\n\t"
    print output

def move():
    # wrapper function for single-player mode
    pickBest(findWords())
