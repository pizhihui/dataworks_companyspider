# encoding=utf-8

import hashlib
import json
import logging
import requests

from urlparse import urljoin
from elasticsearch import Elasticsearch
from redis import Redis
from scrapy_redis.spiders import RedisSpider
from spider.headers import nettyHeader
from spider.items import RawCorpItemLoader
from spider.pyredis import PyRedis

logger = logging.getLogger(__name__)

class QichabaoUrlSpider(RedisSpider):
    '''spider that reads urls from redis queue (myspider:start_urls).'''
    name = 'qichabao_url'
    redis_key = 'qichabao:urls'


    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domans = filter(None, domain.split(','))
        super(QichabaoUrlSpider, self).__init__(*args, **kwargs)
        self.p_url = 'http://qiye.qianzhan.com/'
        # 所有需要查询的公司的名字
        #self.all_company_names = self.get_company_names()


    def get_company_names(self):
        start_urls_tmp = []
        init_url = 'http://qiye.qianzhan.com/search/all/~?o=0&area=0&p=1'
        # 从es取出公司数据
        es_connection = Elasticsearch('10.10.4.148:9200')
        query_all = {
            "query": {
                "match_all": {}
            },
            "collapse": {
                "field": "ent_name_kw"
            },
            "size": 1000,
            # "from": 3
        }
        res = es_connection.search(index='cia_index',
                                        doc_type=['raw_fin_bids', 'raw_fin_info'],
                                        body=query_all,
                                        filter_path=['hits.hits._source.ent_name_kw'])
        for val in res['hits']['hits']:
            tmp_com_name = val['_source']['ent_name_kw'].encode('utf-8')
            row_key = hashlib.new("md5", tmp_com_name).hexdigest()
            data = {
                "command": "getByRowKey",
                "content": {
                    "table": "raw_corp",
                    "rowKey": row_key,
                    "family": "info"
                }
            }
            # 查询hbase是否有该公司,没有加入请求的url中
            res = requests.post('http://10.10.4.168:8986', json=data, headers=nettyHeader)
            if not json.loads(res.content)['result']:
                # 压入redis队列中
                start_urls_tmp.append(init_url.replace('~', tmp_com_name))
                #PyRedis().get_redis().lpush(self.redis_key, start_urls_tmp)

        # tmp_urls = self.append_own_search()
        # tmp_urls.extend(start_urls_tmp)

        logger.error("... start_urls length is: " + str(len(start_urls_tmp)))
        return start_urls_tmp


    def parse(self, response):
        # 根据redis队列中的urls,得到相应,然后xpath取页面上的连接
        el = RawCorpItemLoader(response=response)
        urllist = response.xpath('//div[@class="wrap-f"]//div[@class="listsec_con"]/a[@class="listsec_tit"]/@href').extract()
        for url in urllist[:2]:
            requesturl = urljoin(self.p_url, url)
            # 真正的公司连接放入另外的redis的key中
            PyRedis().get_redis().lpush('qichabao:start_urls', requesturl)

        return el.load_item()