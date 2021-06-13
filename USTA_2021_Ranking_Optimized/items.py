# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Usta2021RankingOptimizedItem(scrapy.Item):
    rank= scrapy.Field()
    bonusPoints=scrapy.Field()
    division= scrapy.Field()
    type=scrapy.Field()
    doublesPoints= scrapy.Field()
    singlesPoints=scrapy.Field()
    district=scrapy.Field()
    name=scrapy.Field()
    combinedPoints=scrapy.Field()
    defaultSection=scrapy.Field()
    rank=scrapy.Field()
    section=scrapy.Field()
    state=scrapy.Field()
    list=scrapy.Field()
    uaid=scrapy.Field()
    city=scrapy.Field()
