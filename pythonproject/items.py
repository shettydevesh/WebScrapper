# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from turtle import title
import scrapy


class PythonprojectItem(scrapy.Item):
    # define the fields for your item here like:
    Number_of_View = scrapy.Field()
    Rating = scrapy.Field()
    Title = scrapy.Field()
    Rank = scrapy.Field()
    
    
