from objs import Movie, Review
from text_analyzer import TextAnalyzer

ta = TextAnalyzer()

class DataManager:
    def __init__(self):
        self.movies = {}

    def process(self, raw_line):
        m = raw_line['movieObj']
        review = Review(raw_line['rating'], raw_line['text'][0])
        try:
            movie = self.movies[m['id']]
        except KeyError:
            movie = Movie(m['id'], m['title'], m['rating'])
            self.movies[m['id']] = movie
        movie.add_review(review)

    def analyze(self):
        for ID in self.movies:
            m = self.movies[ID]
            for i in xrange(len(m.reviews)):
                r = m.reviews[i]
                ta.rank_words(m.rating, r.rating, r.text)
        ta.dump_ranks_to_file()
