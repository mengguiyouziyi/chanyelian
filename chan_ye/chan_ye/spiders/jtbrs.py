# -*- coding: utf-8 -*-
import scrapy
import re
from math import ceil
from scrapy.selector import Selector
from chan_ye.items import DiliItem


class TouzishijianSpider(scrapy.Spider):
	name = 'jtbrs'
	custom_settings = {
		'DEFAULT_REQUEST_HEADERS': {
			'accept': "text/html, */*; q=0.01",
			'accept-encoding': "gzip, deflate",
			'accept-language': "zh-CN,zh;q=0.8",
			'connection': "keep-alive",
			# 'cookie': "PHPSESSID=ulp3a3rs03igg8b0l8nrs3hjg3",
			'host': "hk.56dili.cn",
			'referer': "http://hk.56dili.cn/index2.php?app=public&mod=pub&act=bizs_main&var=%E6%B5%B7%E5%8F%A3%E5%B8%82*1",
			# 'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
			'x-requested-with': "XMLHttpRequest",
			'cache-control': "no-cache",
			'postman-token': "c5e7901c-58a4-f021-947b-bc09867ea969"
		},
	}

	def start_requests(self):
		citys = ['北京市', '上海市', '天津市', '重庆市', '青岛市', '济南市', '苏州市', '南京市', '杭州市', '宁波市', '合肥市', '深圳市', '广州市', '福州市',
		         '厦门市', '南宁市', '海口市', '郑州市', '长沙市', '南昌市', '沈阳市', '大连市', '哈尔滨市', '长春市', '成都市', '昆明市', '贵阳市', '拉萨市',
		         '石家庄市', '保定市', '太原市', '呼和浩特市', '赤峰市', '西安市', '乌鲁木齐市', '兰州市', '银川市', '西宁市']
		js_url = 'http://hk.56dili.cn/index2.php?app=public&mod=citypub&act=graphics&var=1*{}'
		for city in citys:
			url = js_url.format(city)
			print(url)
			yield scrapy.Request(url, meta={'city': city})

	def parse(self, response):
		# print(response.url)
		city = response.meta.get('city')
		cats = ['仓储', '城市公共交通', '道路运输', '管道运输', '航空运输', '水上运输', '铁路运输', '邮政', '装卸搬运和其它']
		nums = re.findall(r'var vses\d = (\d+?);', response.text)
		pages = [ceil(int(num) / 10) for num in nums]
		p_url = 'http://hk.56dili.cn/index2.php?app=public&mod=citypub&act=bizsalllist&var={page}*{city}*{cat}*0*'
		for ind_cat, cat in enumerate(cats):
			ind_cat = ind_cat + 1
			for page in pages:
				if page == 0:
					continue
				for p in range(page):
					url = p_url.format(page=p + 1, city=city, cat=ind_cat)
					print(url)
					yield scrapy.Request(url, callback=self.parse_list, meta={'city': city, 'cat': cat})

	def parse_list(self, response):
		# print(response.url)
		city = response.meta.get('city')
		cat = response.meta.get('cat')
		select = Selector(text=response.text)
		tr_tags = select.xpath('//*[@class="listtable"]//tr')
		for tr in tr_tags:
			item = DiliItem()
			comp_name = tr.xpath('./td[1]//text()').extract()
			addr = tr.xpath('./td[2]//text()').extract()
			property = tr.xpath('./td[3]//text()').extract()
			income = tr.xpath('./td[4]//text()').extract()
			comp_size = tr.xpath('./td[5]//text()').extract()
			item['only_id'] = ''
			item['comp_name'] = _uniteList(comp_name)
			item['addr'] = _uniteList(addr)
			item['property'] = _uniteList(property)
			item['income'] = _uniteList(income)
			item['comp_size'] = _uniteList(comp_size)
			item['city'] = city
			item['cat'] = cat
			yield item


def _solSpace(s):
	return s.strip().replace('\t', '').replace('\r', '').replace('\n', '')


def _uniteList(vl, sep=''):
	vl_1 = sep.join([_solSpace(v) for v in vl if v]) if vl else ''
	return vl_1
