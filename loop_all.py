from oracle import Oracle
from getbest import GuessGenerator
from wordle_dt import Word
from collections import defaultdict
import json

with open('wordle-answers-alphabetical.txt') as f:
    valid_words = [ln.strip() for ln in f]

guesses = defaultdict(list)
for w in valid_words:
    o = Oracle(w)
    attempts = []
    while True:
        with GuessGenerator(*attempts) as gg:
            if len(gg.wordle.valid) == 1:
                assert(o.guess(str(gg.wordle.valid[0])) == (2, 2, 2, 2, 2))
                guesses[w].append(str(gg.wordle.valid[0]))
                print(f'{w} guessed in {len(guesses[w])} attempts')
                break
            g = next(gg)
            attempts.append(f'{g.word}:{"".join([str(x) for x in o.guess(str(g.word))])}')
            guesses[w].append(str(g.word))
with open('all_guesses.json', 'w') as f:
    json.dump(guesses, f, indent=True)