# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

# import scrapy


# class Hw13Item(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass

import scrapy
from scrapy.item import Item, Field

class CompsItem(Item):
    link = Field()
    timestamp = Field()
    title = Field()
    freq_i = Field()
    ram = Field()
    rom = Field()
    price = Field()
    rank = Field()