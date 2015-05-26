class Review:
    def __init__(self, rating, text):
        self.rating = rating
        self.text = text


class Movie:
    def __init__(self, id, title, rating):
        self.id = id
        self.title = title
        self.rating = rating
        self.reviews = list()

    def add_review(self, review):
        self.reviews.append(review)


class Word:
    def __init__(self, word, r):
        self.word = word
        self.rank = r

    def process(self, r):
        tmp = self.rank + r
        self.rank = min(100, max(-100, tmp))  # -100 <= rank <= 100


class WordManager:
    def __init__(self):
        self.words = {}

    def process_word(self, word, r):
        try:
            w = self.words[word]
            w.process(r)
        except KeyError:
            self.words[word] = Word(word, r)

    def get_word_rank(self, word):
        try:
            w = self.words[word]
            return w.rank
        except KeyError:
            return 0

    def get_avg_rank(self):
        sum = 0
        n = len(self.words)
        for i in self.words:
            w = self.words[i]
            sum += w.rank
        return sum / float(n)


from json import JSONEncoder
class JSONEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
