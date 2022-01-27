from wordle_dt import Wordle, Word
from heapq import heappop, heappush
import pickle

with open('wordle-answers-alphabetical.txt') as f:
    valid_words = [Word(ln.strip()) for ln in f]
with open('wordle-allowed-guesses.txt') as f:
    all_words = [Word(ln.strip()) for ln in f]
w = Wordle(valid_words, all_words)
best = w.getBestBranch()
with open('root_wordle.pickle', 'wb') as f:
    pickle.dump(w, f)
bestarr = []
for idx in range(5):
    print(f'{best.word}: {best.entropy}')
    fname = f'root_branch_{best.word}.pickle'
    with open(fname, 'wb') as f:
        pickle.dump(best, f)
    heappop(w.branches)
    bestarr.append(best)
    best = w.getBestBranch()

for b in bestarr:
    heappush(w.branches, b)
with open('root_wordle.pickle', 'wb') as f:
    pickle.dump(w, f)
