# Codenames

Assist tool/solver for Codenames, a board game by Vlaada Chvatil

## How it works

Each word is embedded into a vector space using GloVe. For each word (from the GloVe wiki corpus), we score it against the 25 code names in terms of similarity. We ultimately select the best word and the number of code names that it is associated with.

## How to use it

```
python -i sim.py GLOVE_VECTORS.txt word-list.txt
```

After loading the vectors, in the interpreter run:

```
>>> result = findWord()
>>> result[N][0] // (word, N) is the clue
>>> result[N][3] // These are the words that were associated
```
