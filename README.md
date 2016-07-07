# Codenames

Assist tool/solver for Codenames, a board game by Vlaada Chvatil

## About

Each word is embedded into a vector space using [GloVe](http://nlp.stanford.edu/projects/glove/). For each word (from the GloVe wiki corpus), we score it against the 25 code names in terms of similarity. We ultimately select the best word and the number of code names that it is associated with.

This is a still a crude tool and word associations aren't perfect. As a result, `pickBest` does not always pick the best word. However, there is usually an acceptable clue in the output of `findWords()`.

## Usage

```
python -i sim.py GLOVE_VECTORS.txt word-list.txt
```

After loading the vectors, in the interpreter run:

```
>>> clues = findWords()
>>> pickBest(clues)
('ants', 6)
>>> words
['vet', 'pants', 'cotton', 'platypus', 'grass', 'horse', 'bugle', 'roulette', 'change', 'himalayas', 'fish', 'ninja', 'satellite', 'chest', 'dwarf', 'fan', 'king', 'swing', 'battery', 'bank', 'tooth', 'nurse', 'straw', 'brush', 'scale']
>>> roles
{'bugle': -1, 'battery': -3, 'fish': 1, 'brush': -1, 'cotton': -3, 'vet': -3, 'scale': -3, 'straw': -10, 'chest': -1, 'change': -1, 'nurse': 1, 'pants': 1, 'satellite': 1, 'dwarf': -1, 'horse': 1, 'fan': -1, 'ninja': 1, 'bank': 1, 'king': -3, 'roulette': 1, 'himalayas': -3, 'platypus': -1, 'tooth': 1, 'swing': -3, 'grass': -3}
>>> expected
[(1, 0.4193291853533418, 'fish'), (1, 0.39795848701311254, 'pants'), (1, 0.36527604354032905, 'horse'), (1, 0.2623782121711276, 'tooth'), (1, 0.22965112665806223, 'nurse'), (1, 0.2055846539312118, 'roulette')]
```

In the output for `expected`, the middle value roughly corresponds to the strength of relation. Technically, it is the cosine similarity between the two word vectors, with higher values implying more association and 0 implying independence.

To investigate the other options and word associations:

```
>>> clues[N][0] // (word, N) is the clue
>>> clues[N][3] // Same output format as expected
```

To regenerate a new word list and reassign spies (optional fixed words [w] and assignments [r]):

```
>>> regen(w=[], r=[])
>>> words
['lemon', 'racket', 'atlantis', 'post', 'spot', 'tie', 'pipe', 'octopus', 'straw', 'trunk', 'snow', 'mercury', 'line', 'space', 'bear', 'slip', 'saturn', 'wall', 'giant', 'shoe', 'lead', 'buffalo', 'needle', 'engine', 'chest']
>>> roles
{'straw': -3, 'shoe': -1, 'slip': -1, 'racket': -3, 'line': 1, 'mercury': -1, 'giant': 1, 'lemon': -1, 'lead': -1, 'space': -3, 'snow': -1, 'wall': -3, 'chest': -3, 'tie': 1, 'engine': -3, 'atlantis': 1, 'needle': 1, 'spot': -3, 'bear': 1, 'trunk': -1, 'post': -10, 'saturn': 1, 'octopus': 1, 'pipe': 1, 'buffalo': -3}
```

## Role Mapping

These values are still arbitrary but they could be useful later.


|Value | Role|
|------|-----|
|1     |Your team|
|-1    |Innocent|
|-3    |Other team|
|-10   |Assassin|