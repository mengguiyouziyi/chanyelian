# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DiliItem(scrapy.Item):
	only_id = scrapy.Field()
	city = scrapy.Field()
	cat = scrapy.Field()
	comp_name = scrapy.Field()
	addr = scrapy.Field()
	property = scrapy.Field()
	income = scrapy.Field()
	comp_size = scrapy.Field()


class JiqirenItem(scrapy.Item):
	zhuying = scrapy.Field()
	comp_url = scrapy.Field()
	comp_name = scrapy.Field()
	cat_url = scrapy.Field()
	cat = scrapy.Field()
	loc = scrapy.Field()
	sheng = scrapy.Field()
	shi = scrapy.Field()
	intro = scrapy.Field()


class JqrProductItem(scrapy.Item):
	detail_url = scrapy.Field()
	img_url = scrapy.Field()
	p_name = scrapy.Field()
	brand = scrapy.Field()
	model = scrapy.Field()
	standard = scrapy.Field()
	price = scrapy.Field()
	addr = scrapy.Field()
	time_to = scrapy.Field()
	last_update = scrapy.Field()
	abs = scrapy.Field()
	intro = scrapy.Field()
