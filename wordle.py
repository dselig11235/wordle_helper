#!/usr/bin/python3

import sys, re
from collections import defaultdict

position = sys.argv[1]
others = sys.argv[2]
excluding = sys.argv[3]
matching = []
bypos = [defaultdict(int) for x in range(5)]
any = defaultdict(int)
with open('5_letter_words_freq.txt') as f:
    for ln in f:
        freq, word = ln.split()
        freq = int(freq)
        m = re.match(position, word)
        if m is not None:
            for let in others:
                if let not in word:
                    break
            else:
                for let in excluding:
                    if let in word:
                        break
                else:
                    matching.append((freq, word))
                    for idx, let in enumerate(word):
                        bypos[idx][let] += freq
                        if let not in position:
                            any[let] += freq
best_by_pos = [[y[0] for y in sorted(top.items(), key=lambda x: x[1], reverse=True)[:5]] for top in bypos]
best_any = [y[0] for y in sorted(any.items(), key=lambda x: x[1], reverse=True)[:10]]
anagram = [y[0] for y in sorted([(let, freq) for let, freq in any.items() if let not in others and let not in position and let not in excluding], key=lambda x: x[1], reverse=True)[:10]]
best_matching = [y[1] for y in sorted(matching, key=lambda x: x[0], reverse=True)][:10]
for ln_no in range(max([len(arr) for arr in best_by_pos])):
    print(' '.join([x[ln_no] if len(x) > ln_no else ' ' for x in best_by_pos]))
print()
print(', '.join(best_any))
print(''.join(anagram))
print()
print('\n'.join(best_matching))
