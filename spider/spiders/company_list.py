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


class CompanyListSpider(Spider):

    name = "company_list"
    allowed_domain = ['http://shop.99114.com/']
    start_urls = ["http://shop.99114.com/list/area/101101_1"]

    custom_settings = {
        "DOWNLOADER_MIDDLEWARES":{

        },
        "ITEM_PIPELINES": {
            "spider.pipelines.FileWriterPipeline": 100
        }
    }

    def parse(self, response):
        sel = Selector(response)
        p_url = response.url
        pagenum = 201
        for i in range(1, pagenum + 1):
            requesturl = str(p_url).replace('101101_1', '101101_' + str(i))
            yield Request(requesturl, callback=self.parse_getpages)

    def parse_getpages(self, response):
        sel = Selector(response)
        item = CompanyNameItem()
        name = sel.xpath('//div[@class="wrapper"]//a/strong/text()').extract()
        item['name'] = name
        yield item

