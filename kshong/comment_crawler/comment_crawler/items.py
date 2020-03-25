# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CommentCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    category1 = scrapy.Field()
    category2 = scrapy.Field()
    sympathy_count = scrapy.Field()
    antipathy_count = scrapy.Field()
    comment_no = scrapy.Field()
    contents = scrapy.Field()
    reg_time = scrapy.Field()


    