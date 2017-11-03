# -*- coding: utf-8 -*-

import sys
import urllib
import json
import requests
import logging
from spider.useragent import agents
import random


reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger(__name__)


class Proxies(object):
    def __init__(self):
        self.header = {
            'User-Agent': random.choice(agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate',
        }
        self.test_url = 'https://www.baidu.com/'
        #self.test_url = 'http://qiye.qianzhan.com/'
        self.requestHeader = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"}
        self.daxiang_proxy_url = 'http://vtp.daxiangdaili.com/ip/?tid=556367928768689&num=100&operator=1,2,3&delay=3&filter=off&format=json&longlife=20&protocol=http'
        self.finippool_url = 'http://127.0.0.1:8000/?types=0&count=20&country=国内&protocol=0'
        self.zdaye_url = 'http://10.211.55.3:52880/api.do?filter=1&num=1'
        self.ip_val = []

    def get_proxies_daxiang(self):
        """
        通过大象代理获取ip
        :return:
        """
        res = urllib.urlopen(self.daxiang_proxy_url).read()
        oj = json.loads(res)
        for ip in oj:
            try:
                ip_tmp = 'http://' + ip['host'] + ":" + str(ip['port'])
                requests.get(self.test_url, headers=self.header, proxies={'http': 'http://' + ip_tmp})
                #res = urllib.urlopen(self.test_url, proxies={'http':  ip_tmp}).read()
                self.ip_val.append(ip_tmp)
            except BaseException, e:
                logger.error("---Failure:" + e.message)
                continue

        return self.ip_val

    def get_proxies_finippool(self):
        """
        通过自建ip代理池获取ip
        :return:
        """
        r = requests.get(self.finippool_url)
        ip_ports = json.loads(r.text)
        for ip in ip_ports:
            try:
                ip_tmp = 'http://' + ip[0] + ":" + str(ip[1])
                #res = urllib.urlopen(self.test_url, proxies={'http': ip_tmp}).read()
                requests.get(self.test_url, headers=self.header, proxies={'http': 'http://' + ip_tmp})
                self.ip_val.append(ip_tmp)
            except BaseException, e:
                logger.error("---Failure:" + e.message)
                continue
        return self.ip_val

    def get_proxies_zdaye(self):
        """
        通过站大爷代理获取ip
        :return:
        """
        res = urllib.urlopen(self.zdaye_url).read()
        oj = res.split('\r\n')
        for ip in oj:
            try:
                ip_tmp = 'http://' + ip
                requests.get(self.test_url, headers=self.header, proxies={'http': 'http://' + ip_tmp})
                #res = urllib.urlopen(self.test_url, proxies={'http': ip_tmp}).read()
                self.ip_val.append(ip_tmp)
            except BaseException, e:
                logger.error("---Failure:  {}", e)
                continue

        return self.ip_val

if __name__ == "__main__":
    p = Proxies()
    # ip_val = p.get_proxies_daxiang()
    # outFile = open('verified.txt', 'w')
    # for ip in ip_val:
    #     outFile.write(ip + '\n')
    # outFile.close()
    ip_val = p.get_proxies_zdaye()
    for ip in ip_val:
        print ip
