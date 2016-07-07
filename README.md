# Codenames

Assist tool/solver for Codenames, a board game by Vlaada Chvatil

## About

Each word is embedded into a vector space using [GloVe](http://nlp.stanford.edu/projects/glove/). For each word (from the GloVe wiki corpus), we score it against the 25 code names in terms of similarity. We ultimately select the best word and the number of code names that it is associated with.

This is a still a crude tool and word associations aren't perfect. As a result, `pickBest()` (and `move()` does not always pick the best word. However, there is usually an acceptable clue in the output of `findWords()`.

## Usage

In your shell, run the python interpreter (replace GLOVE_VECTORS.txt with a vector file).

```
python -i sim.py GLOVE_VECTORS.txt word-list.txt
```

### Single-player mode

To view the board:

```
>>> board()
```

To generate the next clue:

```
>>> move()
('accelerates', 3)
```

To guess something:
```
>>> guess('time')
Correct!
```

Rules are currently up to the user to enforce. There is no detection for when the game ends.

### Detailed Usage

After loading the vectors, in the interpreter run:

```
>>> clues = findWords()
>>> pickBest(clues)   //This is the same output of moves()
('ants', 6)
>>> words
['vet', 'pants', 'cotton', 'platypus', 'grass', 'horse', 'bugle', 'roulette', 'change', 'himalayas', 'fish', 'ninja', 'satellite', 'chest', 'dwarf', 'fan', 'king', 'swing', 'battery', 'bank', 'tooth', 'nurse', 'straw', 'brush', 'scale']
>>> roles
{'bugle': (-1, False), 'battery': (-3, False), 'fish': (1, False), 'brush': (-1, False), 'cotton': (-3, False), 'vet': (-3, False), 'scale': (-3, False), 'straw': (-10, False), 'chest': (-1, False), 'change': (-1, False), 'nurse': (1, False), 'pants': (1, False), 'satellite': (1, False), 'dwarf': (-1, False), 'horse': (1, False), 'fan': (-1, False), 'ninja': (1, False), 'bank': (1, False), 'king': (-3, False), 'roulette': (1, False), 'himalayas': (-3, False), 'platypus': (-1, False), 'tooth': (1, False), 'swing': (-3, False), 'grass': (-3, False)}
>>> expected
[(1, 0.4193291853533418, 'fish'), (1, 0.39795848701311254, 'pants'), (1, 0.36527604354032905, 'horse'), (1, 0.2623782121711276, 'tooth'), (1, 0.22965112665806223, 'nurse'), (1, 0.2055846539312118, 'roulette')]
```

In the output of `roles`, the boolean value just indicates that the word has not been guessed yet.

In the output for `expected`, the middle value roughly corresponds to the strength of relation. Technically, it is the cosine similarity between the two word vectors, with higher values implying more association and 0 implying independence.

To investigate the other options and word associations:

```
>>> clues[N][0] // (word, N) is the clue
>>> clues[N][3] // Same output format as expected
```

### Starting a new game

To regenerate a new word list and reassign spies (optional fixed words [w] and assignments [r]):

```
>>> regen(w=[], r=[])
```


### Perf

Global variables `initTime` and `findWordsTime` records the time in seconds to load the interpreter and the time to find the best words.

## Role Mapping

These values are still arbitrary but they could be useful later.


|Value | Role|
|------|-----|
|1     |Your team|
|-1    |Innocent|
|-3    |Other team|
|-10   |Assassin|