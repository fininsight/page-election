

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NavernewsItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    date = scrapy.Field()
    inputdate = scrapy.Field()
    content = scrapy.Field()
    photo = scrapy.Field()
    category1 = scrapy.Field()
    category2 = scrapy.Field()
    oricategory = scrapy.Field()
    url = scrapy.Field()
    media = scrapy.Field()
    summary = scrapy.Field()
    sad = scrapy.Field()
    angry = scrapy.Field()
    want = scrapy.Field()
    like = scrapy.Field()
    warm = scrapy.Field()
    comment = scrapy.Field()
    updatedate = scrapy.Field()
