# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from chan_ye.items import JqrProductItem


class TouzishijianSpider(scrapy.Spider):
	name = 'jqr_product'

	# custom_settings = {
	# 	'DEFAULT_REQUEST_HEADERS': {
	# 		'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
	# 		'accept-encoding': "gzip, deflate",
	# 		'accept-language': "zh-CN,zh;q=0.8",
	# 		'cache-control': "no-cache",
	# 		# 'connection': "keep-alive",
	# 		# 'cookie': "UM_distinctid=15fc95c2872d78-0fdfee884d9db7-31637e01-13c680-15fc95c28748a8; CNZZDATA3130222=cnzz_eid%3D346745979-1510908079-%26ntime%3D1510924313; Hm_lvt_99d3e8dc9c4fb1796f922e4fc84251b1=1510911782; Hm_lpvt_99d3e8dc9c4fb1796f922e4fc84251b1=1510928806; AJSTAT_ok_pages=9; AJSTAT_ok_times=2; __tins__5221700=%7B%22sid%22%3A1510928732944%2C%22vd%22%3A9%2C%22expires%22%3A1510930606401%7D; __51cke__=; __51laig__=10",
	# 		'host': "www.robot-china.com",
	# 		'upgrade-insecure-requests': "1",
	# 		# 'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
	# 		# 'postman-token': "455d07fb-baa0-faf6-92c9-95ea6a2d771c"
	# 	}
	# }

	def start_requests(self):
		urls = ['http://www.robot-china.com/sell/show-{}.html'.format(i) for i in range(12,33500)]
		for url in urls:
			yield scrapy.Request(url, meta={'dont_redirect': True})

	def parse(self, response):
		if response.status == 404:
			return
		select = Selector(text=response.text)
		img_url = select.xpath('//div[@class="xieceprodukuka"]/span/img/@data-src').extract_first()
		p_name = select.xpath('//p[@class="p_title"]/text()').extract_first()
		li_s = select.xpath('//ul[@class="xieceprodutu"]/li')
		brand = ''
		model = ''
		standard = ''
		price = ''
		addr = ''
		time_to = ''
		last_update = ''
		for li in li_s:
			b = li.xpath('./b//text()').extract_first()
			span = li.xpath('./span//text()').extract()
			span = ''.join(span) if span else ''
			if '品   牌：' in b:
				brand = span
			elif '型   号：' in b:
				model = span
			elif '规   格：' in b:
				standard = span
			elif '单   价：' in b:
				price = span
			elif '所在地：' in b:
				addr = span
			elif '有效期至：' in b:
				time_to = span
			elif '最后更新：' in b:
				last_update = span
		abs = select.xpath('//span[@class="xieceproduwz"]//text()').extract()
		abs = ''.join(abs) if abs else ''
		intro = select.xpath('//div[@class="intro"]//text()').extract()
		intro = ''.join(intro) if intro else ''
		item = JqrProductItem()
		item['detail_url'] = response.url
		item['img_url'] = img_url if 'default' not in img_url else ''
		item['p_name'] = p_name.strip() if p_name else ''
		item['brand'] = brand.strip() if brand else ''
		item['model'] = model.strip() if model else ''
		item['standard'] = standard.strip() if standard else ''
		item['price'] = price.strip() if price else ''
		item['addr'] = addr.strip() if addr else ''
		item['time_to'] = time_to.strip() if time_to else ''
		item['last_update'] = last_update.strip() if last_update else ''
		item['abs'] = abs.strip() if abs else ''
		item['intro'] = intro.strip() if intro else ''
		yield item
