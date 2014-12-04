# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


#class FjsenItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
#    pass
# http://doc.scrapy.org/topics/items.html 
from scrapy.item import Item, Field
class FjsenItem(Item):
    # define the fields for your item here like:
    # name = Field()
    id=Field()
    title=Field()
    link=Field()
    addtime=Field()
