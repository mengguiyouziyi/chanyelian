# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DiliItem(scrapy.Item):
	# define the fields for your item here like:
	only_id = scrapy.Field()
	city = scrapy.Field()
	cat = scrapy.Field()
	comp_name = scrapy.Field()
	addr = scrapy.Field()
	property = scrapy.Field()
	income = scrapy.Field()
	comp_size = scrapy.Field()
