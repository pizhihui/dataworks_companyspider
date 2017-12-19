# -*- coding: utf-8 -*-
import datetime
import json
import re

from urlparse import urljoin

from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.selector import Selector
from scrapy import Spider
from scrapy.http import Request
from spider.items import CompanyNameItem
from scrapy.spiders import CrawlSpider


class CompanyListSpiderMinglu(Spider):

    name = "company_list_minglu"
    allowed_domain = ['mingluji.com']
    start_urls = ["https://gongshang.mingluji.com/beijing/list?page=1"]

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "gongshang.mingluji.com",
        "Pragma": "no-cache",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
    }

    custom_settings = {
        "DOWNLOADER_MIDDLEWARES":{

        },
        "ITEM_PIPELINES": {
            "spider.pipelines.FileWriterPipeline": 100
        },
        "DEFAULT_REQUEST_HEADERS":{
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Host": "gongshang.mingluji.com",
            "Pragma": "no-cache",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
        }
    }

    def parse(self, response):
        sel = Selector(response)
        p_url = response.url
        pagenum = 2364
        for i in range(1, pagenum + 1):
            requesturl = str(p_url).replace('page=1', 'page=' + str(i))
            yield Request(requesturl, callback=self.parse_getpages, headers=self.headers)

    def parse_getpages(self, response):
        sel = Selector(response)
        item = CompanyNameItem()
        name = sel.xpath('//div[@class="item-list"]/ol//a/text()').extract()
        item['name'] = name
        yield item

