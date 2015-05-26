# Sentiment Analysis
A basic attempt at Sentiment Analysis to rate text files based on their polarity, using IMDb's reviews to rank words considering the rating given.

### Dependencies:
* [Scrapy](http://scrapy.org/download/)

* [NLTK](http://www.nltk.org/install.html)

### How to use:
1. Crawl all IMDb's reviews using Scrapy (takes ~5 hours to complete)

  ```
  cd crawler
  scrapy crawl imdb -o ../data/all_reviews.json
  ```
2. Set a rank for each token of the reviews

  ```
  cd ../analyzer
  python imdb_analyzer.py ../data/all_reviews.json
  ```
3. Analyze text file and rank it
  
  ```
  python text_analyzer.py <file_to_analyze.txt>
  ```
