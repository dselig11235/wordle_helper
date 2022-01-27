from bitarray import bitarray
from collections import defaultdict
from functools import reduce
from heapq import heappush, heappop
import math

letters = {
    'a': bitarray('00000000000000000000000001'),
    'b': bitarray('00000000000000000000000010'),
    'c': bitarray('00000000000000000000000100'),
    'd': bitarray('00000000000000000000001000'),
    'e': bitarray('00000000000000000000010000'),
    'f': bitarray('00000000000000000000100000'),
    'g': bitarray('00000000000000000001000000'),
    'h': bitarray('00000000000000000010000000'),
    'i': bitarray('00000000000000000100000000'),
    'j': bitarray('00000000000000001000000000'),
    'k': bitarray('00000000000000010000000000'),
    'l': bitarray('00000000000000100000000000'),
    'm': bitarray('00000000000001000000000000'),
    'n': bitarray('00000000000010000000000000'),
    'o': bitarray('00000000000100000000000000'),
    'p': bitarray('00000000001000000000000000'),
    'q': bitarray('00000000010000000000000000'),
    'r': bitarray('00000000100000000000000000'),
    's': bitarray('00000001000000000000000000'),
    't': bitarray('00000010000000000000000000'),
    'u': bitarray('00000100000000000000000000'),
    'v': bitarray('00001000000000000000000000'),
    'w': bitarray('00010000000000000000000000'),
    'x': bitarray('00100000000000000000000000'),
    'y': bitarray('01000000000000000000000000'),
    'z': bitarray('10000000000000000000000000'),
}

all_results = []
result = (0, 0, 0, 0, 0)
while result != (2, 2, 2, 2, 2):
    all_results.append(result)
    new_result = list(result)
    new_result[4] = int(result[4]) + 1
    while 3 in new_result:
        idx = new_result.index(3)
        new_result[idx] = 0
        new_result[idx-1] += 1
    result = tuple(new_result)


class Word:
    def __init__(self, word):
        self.word = word
        self.position = []
        self.has = bitarray('0')*26    
        for let in word:
            self.position.append(letters[let])
            self.has |= letters[let]
    def __str__(self):
        return self.word
    def __repr__(self):
        return self.word

class Branch:
    def __init__(self, word, valid_words, all_words):
        self.word = word
        self.valid_words = valid_words
        self.all_words = all_words
        self.responses = defaultdict(list)
        self.result_iter = iter(all_results)
        self.entropy = 0
        self.count = 0
        self.cur_result = ()
        self.total_words_in_branches = 0
    def nextResponse(self):
        self.count += 1
        result = next(self.result_iter)
        self.cur_result = result
        #print(f'evaluating {result} in {self.word}')
        pos_to_match = bitarray()
        matches_somewhere = bitarray('0')*26
        matches_nowhere = bitarray('0')*26
        for pos in range(5):
            if result[pos] == 2:
                pos_to_match += self.word.position[pos]
                matches_somewhere |= self.word.position[pos]
            elif result[pos] == 1:
                pos_to_match += ~self.word.position[pos]
                matches_somewhere |= self.word.position[pos]
            else:
                pos_to_match += ~self.word.position[pos]
                matches_nowhere |= self.word.position[pos]
        for target_word in self.valid_words:
            target_pos = reduce(lambda a, b: a+b, target_word.position)
            if target_pos | pos_to_match != pos_to_match:
                continue
            if matches_somewhere & target_word.has != matches_somewhere:
                continue
            if matches_nowhere & target_word.has != bitarray('0')*26:
                continue
            self.responses[result].append(target_word)
        if len(self.responses[result]) > 0:
            self.entropy += (-math.log(1/len(self.responses[result]))/math.log(2)) * (len(self.responses[result])/len(self.valid_words))
            self.total_words_in_branches += len(self.responses[result])
        remaining_words = len(self.valid_words) - self.total_words_in_branches
        remaining_branches = len(all_results) - self.count
        self.estimate = self.entropy
        if remaining_branches > 0:
            min_words_per_branch = int(remaining_words/remaining_branches)
            if min_words_per_branch > 0:
                self.estimate += (-math.log(1/min_words_per_branch)/math.log(2)) * (remaining_words/len(self.valid_words))
        return True

class Wordle:
    def __init__(self, valid_words, all_words):
        self.valid = valid_words
        self.all = all_words
        self.branches = []
        for idx, word in enumerate(self.all):
            heappush(self.branches, (0, idx, Branch(word, self.valid, self.all)))
    def getBestBranch(self):
        longest_branch_len = -1
        longest_branch = None
        while True:
            entropy, idx, best_branch = heappop(self.branches)
            try:
                while(True):
                    if best_branch.nextResponse():
                        break
                if best_branch.count > longest_branch_len:
                    longest_branch = best_branch
                    longest_branch_len = best_branch.count
                def branchInfo(b):
                    return f'{b.word}:{b.cur_result}={b.entropy:.2f}[{b.estimate:.2f}]'
                print(f'longest: {branchInfo(longest_branch)}, current: {branchInfo(best_branch)}')
            except StopIteration:
                return best_branch
            finally:
                heappush(self.branches, (best_branch.estimate, idx, best_branch))