from objs import WordManager, JSONEncoder
import re
import json

wm = WordManager()

class TextAnalyzer:
    def __init__(self):
        pass

    def rank_words(self, global_rating, rating, text):
        r = self.get_rank(global_rating, rating)
        for w in self.get_words_list(text):
            wm.process_word(w, r)

    def dump_ranks_to_file(self):
        j = json.dumps(wm.words.values(), cls=JSONEncoder)
        with open('../data/ranked_words.json', 'w') as f:
            f.write(j)

    def analyze_text(self, text):
        a_wm = WordManager()
        with open('../data/ranked_words.json', 'r') as f:
            j = json.loads(f.read())
            for l in j:
                a_wm.process_word(l['word'], l['rank'])
            print "Average rank: " + str(a_wm.get_avg_rank())
            l = self.get_words_list(text)
            sum = 0
            n = len(l)
            for w in l:
                sum += a_wm.get_word_rank(w)
            avg = sum / float(n)
            print "Text rank: " + str(avg) + ", normalized: " + str((avg + 100) / float(2))

    @staticmethod
    def get_words_list(text):
        import nltk
        l = nltk.word_tokenize(text)
        return l

    @staticmethod
    def get_rank(movie_rating, review_rating):
        import math
        r = max((100 - math.pow((math.fabs(movie_rating - review_rating) / 6.8), 3)) / float(100), 0)
        return r * -1 if review_rating < 55 else 1

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print "Error: Expecting file as parameter."
        sys.exit(1)
    with open(sys.argv[1], 'r') as f:
        ta = TextAnalyzer()
        text = f.read()
        ta.analyze_text(text)
