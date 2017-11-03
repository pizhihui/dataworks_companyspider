# -*- coding: utf-8 -*-

import json
import logging
import requests
import datetime
import hashlib
from scrapy.loader.processors import TakeFirst, MapCompose
from scrapy_redis.spiders import RedisSpider
from spider.items import RawCorpItem, RawCorpItemLoader
from spider.pyredis import PyRedis


req = requests.session()


class QichabaoSpider(RedisSpider):
    name = 'qichabao_com'
    allowed_domains = ["qianzhan.com"]
    redis_key = 'qichabao:start_urls'

    specialHeader = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Length": "55",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "qiye.qianzhan.com",
        "Origin": "http://qiye.qianzhan.com",
        "Pragma": "no-cache",
        "Referer": "http://qiye.qianzhan.com/orgcompany/searchitemdtl/4dfbc09e9d23816a342a338d4f8f13b8.html",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"

    }

    req_cookies = json.loads(PyRedis().get_redis().get("qichabao:Cookies"))

    def parse(self, response):
        coding = response.encoding
        url = response.url
        # item = RawCorpItem()
        # l = ItemLoader(item=item, response=response)
        # l.default_output_processor = TakeFirst()

        l = RawCorpItemLoader(response=response)
        # 公司名称
        l.add_xpath('gsmc', '//div[@class="arthd_con"]/div[@class="arthd_tit"]/h1/text()')
        # 电话
        l.add_xpath('dh', '//div[@class="arthd_con"]/div[@class="arthd_info"][1]/span/text()')
        # 邮箱
        # l.add_xpath('yx', '')
        l.add_value('yx', '')
        # 官网
        l.add_xpath('gw', '//div[@class="arthd_con"]/div[@class="arthd_info"][2]/a/text()')
        # 上市详情
        # l.add_xpath('ssxq', '')
        l.add_value('ssxq', '')
        # 统一社会信用代码
        l.add_xpath('tyshxydm', '//li[@class="xydm"][1]/span[2]/text()')
        # 纳税人识别号
        l.add_xpath('nsrsbh', '//li[@class="xydm"][2]/span[2]/text()')
        # 注册号
        l.add_xpath('zch', '//ul[@class="art-basic"]/li[3]/span[2]/text()')
        # 组织机构代码
        l.add_xpath('zzjgdm', '//ul[@class="art-basic"]/li[4]/span[2]/text()')
        # 法定代表人
        l.add_xpath('fddbr', '//ul[@class="art-basic"]/li[6]/span[2]/a/text()')
        # 注册资本
        l.add_xpath('zczb', '//ul[@class="art-basic"]/li[9]/span[2]/text()')
        # 经营状态
        l.add_xpath('jyzt', '//ul[@class="art-basic"]/li[8]/span[2]/text()')
        # 成立日期
        l.add_xpath('clrq', '//ul[@class="art-basic"]/li[10]/span[2]/text()')
        # 公司类型
        l.add_xpath('gslx', '//ul[@class="art-basic"]/li[7]/span[2]/text()')
        # 人员规模
        l.add_value('rygm', '')
        # 营业期限
        l.add_xpath('yyqx', '//ul[@class="art-basic"]/li[12]/span[2]/text()')
        # 登记机关
        l.add_xpath('djjg', '//ul[@class="art-basic"]/li[11]/span[2]/text()')
        # 核准日期
        l.add_xpath('hzrq', '//ul[@class="art-basic"]/li[14]/span[2]/text()')
        # 英文名
        l.add_value('ywm', '')
        # 所属地区
        l.add_xpath('ssdq', '//ul[@class="art-basic"]/li[13]/span[2]/text()')
        # 所属行业
        l.add_xpath('sshy', '//section[@class="pb-d2"]/ul[2]/li[1]/span[2]//a/text()')
        # 企业地址
        l.add_xpath('qydz', '//ul[@class="art-basic"]/li[15]/span[2]/text()')
        # 经营范围
        l.add_xpath('jyfw', '//ul[@class="art-basic"]/li[16]/span[2]/text()')

        # 股东信息 gdxx {'gdxm':'','rjcze':'', 'sjcze':'','gdlx':''}
        gdxx = []
        if l.get_xpath('//*[@id="M_gdxx"]'):
            gdxm_list = l.get_xpath('//div[@class="art-shareholder"]//em[@class="name"]/a/text()')
            rjcze_list = l.get_xpath('//div[@class="art-shareholder"]//div[@class="capital"]/p[1]/text()')
            sjcze_list = l.get_xpath('//div[@class="art-shareholder"]//div[@class="capital"]/p[2]/text()')
            gdlx_list = l.get_xpath('//div[@class="art-shareholder"]//span[@class="info"]/text()')
            if not gdlx_list:
                for gdxm, rjcze, sjcze in zip(gdxm_list, rjcze_list, sjcze_list):
                    gdxx_dic = {}
                    gdxx_dic['gdxm'] = gdxm.strip()
                    gdxx_dic['rjcze'] = rjcze[rjcze.find('：') + 1:].strip()
                    gdxx_dic['sjcze'] = sjcze[sjcze.find('：') + 1:].strip()
                    gdxx_dic['gdlx'] = ''
                    gdxx.append(gdxx_dic)
            else:
                for gdxm, rjcze, sjcze, gdlx in zip(gdxm_list, rjcze_list, sjcze_list, gdlx_list):
                    gdxx_dic = {}
                    gdxx_dic['gdxm'] = gdxm.strip()
                    gdxx_dic['rjcze'] = rjcze[rjcze.find('：') + 1:].strip()
                    gdxx_dic['sjcze'] = sjcze[sjcze.find('：') + 1:].strip()
                    gdxx_dic['gdlx'] = gdlx.strip()
                    gdxx.append(gdxx_dic)
            l.add_value('gdxx', json.dumps(gdxx, ensure_ascii=False))

        # 主要成员 js动态获取,根据网站


        try:
            org_code = response.url[-37:response.url.rfind('.')]
            oc_area = l.get_xpath('//input[@id="hdoc_area"]/@value')[0]
            zycy_search_url = 'http://qiye.qianzhan.com/orgcompany/searchitemcyxx'
            self.specialHeader['Referer'] = url
            respon = req.post(zycy_search_url, headers=self.specialHeader, cookies=self.req_cookies,
                              data={'orgCode': org_code, 'oc_area': oc_area})
            zycy_res_obj = json.loads(respon.content)

            zycy = []
            if zycy_res_obj['code'] == 200:
                for val in zycy_res_obj['dataList']:
                    zycy_dic = {}
                    zycy_dic['xm'] = val['om_name']
                    zycy_dic['zw'] = val['om_position']
                    zycy.append(zycy_dic)
            l.add_value('zycy', json.dumps(zycy, ensure_ascii=False))
        except BaseException, e:
            logging.exception("company's zycy info error: %s", e)
            l.add_value('zycy', '[]')

        # 变更信息
        bgxx = []
        if l.get_xpath('//*[@id="M_bgxx"]'):
            bgrq_list = l.get_xpath('//*[@id="M_bgxx"]//time[@class="time"]/text()')
            bgq_list = l.get_xpath('//*[@id="M_bgxx"]//div[@class="before"]/p/text()', MapCompose(unicode.strip))
            bgh_list = l.get_xpath('//*[@id="M_bgxx"]//div[@class="after"]/p/text()', MapCompose(unicode.strip))
            bgxm_list = l.get_xpath('//*[@id="M_bgxx"]//p[@class="info"]/text()')
            for bgrq, bgg, bgh, bgxm in zip(bgrq_list, bgq_list, bgh_list, bgxm_list):
                bgxx_dic = {}
                bgxx_dic['bgrq'] = bgrq
                bgxx_dic['bgg'] = bgg
                bgxx_dic['bgh'] = bgh
                bgxx_dic['bgxm'] = bgxm
                bgxx.append(bgxx_dic)
            l.add_value('bgxx', json.dumps(bgxx, ensure_ascii=False))

        # 分支机构名称
        fzjgmc = []
        if l.get_xpath('//*[@id="M_fzjg"]'):
            fzjgmc_list = l.get_xpath('//*[@id="M_fzjg"]//p[@class="tit"]/a/text()')
            for val in fzjgmc_list:
                fzjgmc.append(val)
            l.add_value('fzjgmc', json.dumps(fzjgmc, ensure_ascii=False))

        # 公司简介
        l.add_xpath('gsjj', '//*[@id="M_gsjj"]/div[2]/p/p/text()')

        # 对外投资信息, js动态获取
        dwtz = []
        dwtz_search_url = 'http://qiye.qianzhan.com/orgcompany/searchitemdftz'
        org_name = (l.get_xpath('//div[@class="arthd_con"]/div[@class="arthd_tit"]/h1/text()')[0]).encode(
            "utf-8").decode('utf-8')
        page_size = 20
        self.specialHeader[
            'Referer'] = 'http://qiye.qianzhan.com/orgcompany/searchitemdtl/6b554c19abf167223b299aea0dfffa40.html'
        respon = req.post(dwtz_search_url, headers=self.specialHeader, cookies=self.req_cookies,
                          data={'orgName': str(org_name), 'page': 1, 'pageSize': page_size})
        if respon.content:
            try:

                dwtz_res_obj = json.loads(respon.content)
                loop_counts = dwtz_res_obj['rowCount'] / page_size + 1  # 获取总页数
                for page in range(1, loop_counts + 1):
                    # 直接发送post请求
                    respon = req.post(dwtz_search_url, headers=self.specialHeader, cookies=self.req_cookies,
                                      data={'orgName': str(org_name), 'page': page, 'pageSize': page_size})
                    res_obj = json.loads(respon.content)
                    if res_obj['code'] == 200:
                        for val in res_obj['dataList']:
                            dwtz.append(val['name'])
                l.add_value('dwtz', json.dumps(dwtz, ensure_ascii=False))
            except BaseException, e:
                logging.exception("company's dwtz info error: %s", e)
                l.add_value('dwtz', '[]')

        l.add_value('url', url)
        l.add_value('spider_name', 'qichabao_com')
        l.add_value('crawltime', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        l.add_value('source_domain', 'qiye.qianzhan.com^深圳企查宝数据科技有限公司')
        item = l.load_item()
        #gsmc = item['gsmc']


        yield item



