from wordle_dt import Wordle, Word
from heapq import heappop, heappush
import sys
import os
import pickle

class GuessGenerator:
    def __init__(self, *attempts):
        attempts = list(attempts)
        with open('wordle-allowed-guesses.txt') as f:
            all_words = [Word(ln.strip()) for ln in f]
        self.outfile = f'{".".join(["root_wordle", *attempts])}.pickle'
        if os.path.exists(self.outfile):
            with open(self.outfile, 'rb') as f:
                self.wordle = pickle.load(f)
        elif len(attempts) == 0:
            with open('wordle-answers-alphabetical.txt') as f:
                valid_words = [Word(ln.strip()) for ln in f]
            self.wordle = Wordle(valid_words, all_words)
        else:
            self.last_attempt = attempts.pop()
            last_word, last_response = self.last_attempt.split(':')
            self.stem = f'{".".join(attempts)}'
            if len(self.stem) > 0:
                self.stem = f'.{self.stem}'
            fname = f'root_wordle{self.stem}.pickle'
            with open(fname, 'rb') as f:
                w = pickle.load(f)
            branch = [b for b in w.branches if str(b[2].word) == last_word][0][2]
            try:
                while True:
                    branch.nextResponse()
            except StopIteration:
                pass
            self.wordle = Wordle(branch.responses[tuple([int(x) for x in last_response])], all_words)
    def __enter__(self):
        self.bestarr = []
        return self
    def __iter__(self):
        return self
    def __next__(self):
        best = self.wordle.getBestBranch()
        best_tpl = heappop(self.wordle.branches)
        self.bestarr.append(best_tpl)
        return best
    def __exit__(self, exc_type, exc_value, traceback):
        for b in self.bestarr:
            heappush(self.wordle.branches, b)
        with open(self.outfile, 'wb') as f:
            pickle.dump(self.wordle, f)

if __name__ == '__main__':
    with GuessGenerator(*sys.argv[1:]) as guesser:
        if len(guesser.wordle.valid) < 35:
            print('Valid words:')
            for word in guesser.wordle.valid:
                print(f'\t{word}')
            answer = input('Continue to generate best guesses? [yes/no]: ')
            if answer != 'yes':
                exit(0)
        guesses = []
        while True:
            for idx in range(5):
                guesses.append(next(guesser))
            answer = input('Generate more? [yes/no]: ')
            for guess in guesses:
                print(f'{guess.word}: {guess.entropy}')
            if answer == 'no':
                break
            else:
                guesses = []