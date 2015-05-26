# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImdbMovie(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    reviews_url = scrapy.Field()
    number_of_reviews = scrapy.Field()
    title = scrapy.Field()
    rating = scrapy.Field()

class ImdbReview(scrapy.Item):
    movieObj = scrapy.Field()
    text = scrapy.Field()
    rating = scrapy.Field()
