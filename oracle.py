class Oracle:
    def __init__(self, word):
        self.word = word
    def guess(self, guess):
        response = []
        for idx, let in enumerate(guess):
            if let == self.word[idx]:
                response.append(2)
            elif let in self.word:
                response.append(1)
            else:
                response.append(0)
        return tuple(response)