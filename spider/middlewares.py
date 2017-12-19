# -*- coding: utf-8 -*-

import json
import logging
import os
import random
import time

import redis
import requests
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware  # 代理ip，这是固定的导入
from scrapy.downloadermiddlewares.retry import RetryMiddleware # 重试机制, 固定导入
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware  # 代理UA，固定导入

from spider.proxyip.proxyipvalidate import Proxies
from useragent import agents
from cookies import QichabaoCookie
from spider.pyredis import PyRedis

logger = logging.getLogger(__name__)

class IPPOOLS(HttpProxyMiddleware):

    def __init__(self, ip=''):
        super(IPPOOLS, self).__init__()
        #self.use_xundaili()
        self.ip = ip

    def process_request(self, request, spider):
        """使用代理ip，随机选用"""
        proxy = self.get_random_proxy()
        print "reuquest随机的ip是: " + proxy
        try:
            request.meta["proxy"] = proxy
        except Exception, e:
            pass

    def process_response(self, request, response, spider):
        """对返回的response处理"""
        # 如果返回的response状态不是200，重新生成当前request对象
        if response.status != 200:
            proxy = self.get_random_proxy()
            # 对当前request加上代理
            request.meta["proxy"] = proxy
            print "response随机的ip是: " + proxy
            return request
        return response

    def get_random_proxy(self):
        """随机从代理池中读取proxy"""
        p = Proxies()
        proxies = p.get_proxies_zdaye()
        # while True:
        #     try:
        #         proxies = p.get_proxies_zdaye()
        #         #proxy = random.choice(proxies).strip()
        #         requests.get("http://qiye.qianzhan.com/",proxies={'http': proxies})
        #         break
        #     except BaseException:
        #         continue

        # while 1:
        #     proxies = p.get_proxies_zdaye()
        #     if proxies:
        #         break
        #     else:
        #         time.sleep(1)
        #
        # while True:
        #     #proxies = p.get_proxies_daxiang()
        #     #proxies = p.get_proxies_finippool()
        #     try:
        #         proxy = random.choice(proxies).strip()
        #         response = requests.get('https://www.baidu.com', proxies={'http': 'http://' + proxy})
        #         break
        #     except BaseException, e:
        #         continue

        return proxies

    def get_random_proxy_byfile(self):
        """
        从文件中随机获取ip
        :return:
        """
        while 1:
            file_path = os.getcwd() + "/verified.txt"
            with open(file_path, 'r') as f:
                proxies = f.readlines()
            if proxies:
                break
            else:
                time.sleep(1)
        proxy = ''
        while True:
            try:
                proxy = random.choice(proxies).strip()
                response = requests.get('https://www.baidu.com', proxies={'http': 'http://' + proxy})
                #res = urllib.urlopen('https://www.baidu.com', proxies={'http': 'https://' + proxy}).read()
                break
            except BaseException, e:
                continue
        #return {"http": "http://" + proxy, "https": "https://" + proxy}

        return "http://" + proxy

class UAPOOLS(UserAgentMiddleware):
    """ 自定义切换agent """
    def process_request(self, request, spider):
        agent = random.choice(agents)
        try:
            request.headers.setdefault('User-Agent', agent)
        except Exception, e:
            # print e
            pass


class QichabaoCookieMiddleware(RetryMiddleware):
    """ 企查宝的cookie连接池, 存储到redis里, 从redis里获取cookie """
    def __init__(self, settings, crawler):
        RetryMiddleware.__init__(self, settings)
        #self.rconn = redis.from_url(settings['REDIS_URL'], db=1, decode_responses=True)  ##decode_responses设置取出的编码为str
        # 首次登陆获取cookies
        res = QichabaoCookie().init_cookie()
        # 存入redis中
        PyRedis().get_redis().set("qichabao:Cookies", json.dumps(res,ensure_ascii=False))


    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler)

    def process_request(self, request, spider):
        json_str = PyRedis().get_redis().get("qichabao:Cookies")
        request.cookies = json.loads(json_str)
        # redisKeys = self.rconn.keys()
        # while len(redisKeys) > 0:
        #     elem = random.choice(redisKeys)
        #     if spider.name + ':Cookies' in elem:
        #         cookie = json.loads(self.rconn.get(elem))
        #         request.cookies = cookie
        #         request.meta["accountText"] = elem.split("Cookies:")[-1]
        #         break