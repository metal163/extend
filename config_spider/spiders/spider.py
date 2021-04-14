# -*- coding: utf-8 -*-
import scrapy
import re
from config_spider.items import Item
from urllib.parse import urljoin, urlparse

def get_real_url(response, url):
    if re.search(r'^https?', url):
        return url
    elif re.search(r'^\/\/', url):
        u = urlparse(response.url)
        return u.scheme + ":" + url
    return urljoin(response.url, url)

class ConfigSpider(scrapy.Spider):
    name = 'config_spider'

    def start_requests(self):
        yield scrapy.Request(url='http://news.163.com/special/0001386F/rank_news.html??metal', callback=self.parse_list)

    def parse_list(self, response):
        prev_item = response.meta.get('item')
        for elem in response.css('table tr:not(:first-child)'):
            item = Item()
            item['title'] = elem.css('td:nth-child(1) > a::text').extract_first()
            item['url'] = elem.css('td:nth-child(1) > a::attr("href")').extract_first()
            item['clicks'] = elem.css('td.cBlue::text').extract_first()
            if prev_item is not None:
                for key, value in prev_item.items():
                    item[key] = value
            yield item


