# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RobotsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class XingItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()


class ZdicWordItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    url = scrapy.Field()
    bushou = scrapy.Field()
    bihua = scrapy.Field()
    jiegou = scrapy.Field()
    is_cichangyong = scrapy.Field()
    is_changyong = scrapy.Field()
    is_tongyong = scrapy.Field()
    pinyins = scrapy.Field()
    fanti = scrapy.Field()
    jieshi = scrapy.Field()
