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
            best = None
            for g in gg:
                if g.entropy > 0:
                    if lastg is None:
                        best = g
                    break
                elif str(g.word) in valid_words:
                    best = g
                    break
                else:
                    best = g
            response = o.guess(str(best.word))
            if response == (2, 2, 2, 2, 2):
                guesses[w].append(str(best.word))
                print(f'{w} guessed in {len(guesses[w])} attempts')
                break
            else:
                attempts.append(f'{g.word}:{"".join([str(x) for x in o.guess(str(g.word))])}')
                guesses[w].append(str(g.word))
                    
with open('all_guesses.json', 'w') as f:
    json.dump(guesses, f, indent=True)