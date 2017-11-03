# -*- coding: utf-8 -*-
import requests
import json
import redis
import logging
from spider.rk import RClient
from spider.pyredis import PyRedis

logger = logging.getLogger(__name__)


class QichabaoCookie(object):



    def __init__(self):
        self.header = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
            "Connection": "keep-alive",
            "Host": "qiye.qianzhan.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0",
        }
        self.loginHeader = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Content-Length": "74",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "qiye.qianzhan.com",
            "Referer": "http://qiye.qianzhan.com/usercenter/login",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0",
            "X-Requested-With": "XMLHttpRequest"
        }
        self.requestHeader = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Connection": "keep-alive",
            "Host": "qiye.qianzhan.com",
            "Referer": "http://qiye.qianzhan.com/",
            "Upgrade-Insecure-Requests": "1",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0"
        }
        self.req = requests.Session()
        self.login_url = ""
        self.baseUrl = 'http://qiye.qianzhan.com/usercenter/login'
        self.codeurl = 'http://qiye.qianzhan.com/usercenter/varifyImage?t=ssologin.js(v1.4.18)'
        self.loginurl = 'http://qiye.qianzhan.com/usercenter/dologin'
        self.checkUrl = 'http://qiye.qianzhan.com/search/all/~?o=0&area=11&p=1'
        self.req_cookies = {}


    ## 登录,获取Cookie
    def post_login(self):
        base = self.req.get(self.baseUrl, headers=self.header)
        # valcode = self.req.get(self.codeurl, headers=self.header,
        #                   cookies=requests.utils.dict_from_cookiejar(base.cookies))
        valcode = self.req.get(self.codeurl, headers=self.header)

        rc = RClient('pizhihui', 'pizhihui@313', '89269', 'fac1e378fbb641deae6846d07c88d21c')
        code = rc.rk_create(valcode.content, 3040)['Result']

        data = {
            "userId": "18910781722",
            "password": "pizhihui@313",
            "VerifyCode": str(code),
            "sevenDays": "false",
            "redir": "http://qiye.qianzhan.com/"
        }

        resp = self.req.post(self.loginurl, headers=self.loginHeader,
                        cookies=requests.utils.dict_from_cookiejar(base.cookies),
                        data=data)
        # self.req_cookies = dict(base.cookies.get_dict(), **resp.cookies.get_dict())
        self.req_cookies = self.req.cookies.get_dict()

        if resp.content.find("true") != -1:
            logger.info("login in success: %s", json.dumps(resp.content, ensure_ascii=False))
            flag = True
        else:
            logger.error("login in fail: %s", json.dumps(resp.content, ensure_ascii=False))
            flag = False
        return flag
        #cookies = final_cookies.get_dict()
        #logger.warning("获取Cookie成功！（账号为:%s）" % account)
        #return json.dumps(final_cookies)



    def init_cookie(self):
        json_str = PyRedis().get_redis().get("qichabao:Cookies")
        res = {}
        resp = self.req.get(self.checkUrl, headers=self.requestHeader, cookies=json.loads(json_str))
        # cookie过期
        if resp.content.find("verifycode") != -1:
            logger.error("需要重新登录")
            while True:
                logger.info("登录中.....")
                if self.post_login():
                    res = self.req_cookies
                    break
        # cookie没有过期
        else:
            res = json.loads(json_str)
        return res

        # redkeys = reds.keys()
        # for user in redkeys:
        #     password = reds.get(user)
        #     if red.get("%s:Cookies:%s--%s" % (spidername, user, password)) is None:
        #         cookie = self.get_cookie(user, password)
        #         red.set("%s:Cookies:%s--%s"% (spidername, user, password), cookie)


    def update_cookie(self, red, accountText, spidername):
        red = redis.Redis()
        pass

    def remove_cookie(self, red, spidername, accountText):
        #red = redis.Redis()
        red.delete("%s :Cookies: %s" % (spidername, accountText))
        pass


