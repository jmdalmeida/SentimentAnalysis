import scrapy
from texteval.items import ImdbMovie, ImdbReview
import urlparse
import math
import re


class ImdbSpider(scrapy.Spider):
    name = "imdb"
    allowed_domains = ["imdb.com"]
    start_urls = [
        # "http://www.imdb.com/chart/top",
        # "http://www.imdb.com/chart/bottom"
        "http://www.imdb.com/search/title?at=0&count=100&sort=alpha&title_type=feature,tv_series,tv_movie"
    ]
    DOWNLOADER_MIDDLEWARES = {
        'scrapy.contrib.downloadermiddleware.robotstxt.ROBOTSTXT_OBEY': True,
    }
    base_url = "http://www.imdb.com"

    def parse(self, response):
        movies = response.xpath("//*[@id='main']/table/tr/td[3]/a/@href")
        for i in xrange(len(movies)):
            l = self.base_url + movies[i].extract()
            print l
            request = scrapy.Request(l, callback=self.parse_movie)
            yield request

        next = response.xpath("//*[@id='right']/span/a")[-1]
        next_url = self.base_url + next.xpath(".//@href")[0].extract()
        next_text = next.xpath(".//text()").extract()[0][:4]
        if next_text == "Next":
            request = scrapy.Request(next_url, callback=self.parse)
            yield request
        '''
        for sel in response.xpath("//table[@class='chart']/tbody/tr"):
            url = urlparse.urljoin(response.url, sel.xpath("td[2]/a/@href").extract()[0].strip())
            request = scrapy.Request(url, callback=self.parse_movie)
            yield request
        '''

    def parse_movie(self, response):
        movie = ImdbMovie()
        i1 = response.url.find('/tt') + 1
        i2 = response.url.find('?')
        i2 = i2 - 1 if i2 > -1 else i2
        movie['id'] = response.url[i1:i2]
        movie['url'] = "http://www.imdb.com/title/" + movie['id']
        r_tmp = response.xpath("//div[@class='titlePageSprite star-box-giga-star']/text()")
        if r_tmp is None or r_tmp == "" or len(r_tmp) < 1:
            return
        movie['rating'] = int(float(r_tmp.extract()[0].strip()) * 10)
        movie['title'] = response.xpath("//span[@itemprop='name']/text()").extract()[0]
        movie['reviews_url'] = movie['url'] + "/reviews"
        # Number of reviews associated with this movie
        n = response.xpath("//*[@id='titleUserReviewsTeaser']/div/div[3]/a[2]/text()")
        if n is None or n == "" or len(n) < 1:
            return
        n = n[0].extract().replace("See all ", "").replace(" user reviews", "")\
            .replace(" user review", "").replace(",", "").replace(".", "").replace("See ", "")
        if n == "one":
            n = 1
        else:
            n = int(n)
        movie['number_of_reviews'] = n
        r = int(math.ceil(n / 10))
        for x in xrange(1, r):
            start = x * 10 - 10
            url = movie['reviews_url'] + "?start=" + str(start)
            request = scrapy.Request(url, callback=self.parse_review)
            request.meta['movieObj'] = movie
            yield request

    def parse_review(self, response):
        ranks = response.xpath("//*[@id='tn15content']/div")[0::2]
        texts = response.xpath("//*[@id='tn15content']/p")
        del texts[-1]
        if len(ranks) != len(texts):
            return

        for i in xrange(0, len(ranks) - 1):
            review = ImdbReview()
            review['movieObj'] = response.meta['movieObj']
            review['text'] = texts[i].xpath("text()").extract()
            rating = ranks[i].xpath(".//img[2]/@src").re("-?\\d+")
            if rating is None or rating == "" or len(rating) < 1:
                return
            review['rating'] = int(rating[0])
            yield review
