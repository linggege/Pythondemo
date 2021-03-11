# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TodaymovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass

    # movieTitleCn = scrapy.Field()  # 影片中文名
    # movieTitleEn = scrapy.Field()  # 影片英文名
    # director = scrapy.Field()  # 导演
    # runtime = scrapy.Field()  # 电影时长
    yclr = scrapy.Field()
    ycjzc = scrapy.Field()