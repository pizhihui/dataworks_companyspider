# -*- coding: utf-8 -*-

from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join

from scrapy.item import Item, Field
from scrapy.exceptions import DropItem




class RequiredFieldItem(Item):
    def validate(self):
        for required_field in self.required_fields:
            if required_field not in self or self[required_field] is None:
                raise DropItem('not field %s' % required_field)

class CompanyNameItem(Item):
    name = Field()

class HBaseItem(RequiredFieldItem):

    # hbase 表名
    table_name = None

    # hbase 列族
    column_family = 'column'

    # md5后作为主键的列
    row_key_field = None

    def get_row_key(self):
        return self[self.row_key_field]

class RawCorpItem(HBaseItem):
    # hbase 用到的字段
    table_name = 'raw_corp'
    column_family = 'info'
    required_fields = ['gsmc', 'spider_name']

    # 公司名称
    gsmc = Field()
    # 电话
    dh = Field()
    # 邮箱
    yx = Field()
    # 官网
    gw = Field()
    # 上市详情
    ssxq = Field()
    # 统一社会信用代码
    tyshxydm = Field()
    # 纳税人识别号
    nsrsbh = Field()
    # 注册号
    zch = Field()
    # 组织机构代码
    zzjgdm = Field()
    # 法定代表人
    fddbr = Field()
    # 注册资本
    zczb = Field()
    # 经营状态
    jyzt = Field()
    # 成立日期
    clrq = Field()
    # 公司类型
    gslx = Field()
    # 人员规模
    rygm = Field()
    # 营业期限
    yyqx = Field()
    # 登记机关
    djjg = Field()
    # 核准日期
    hzrq = Field()
    # 英文名
    ywm = Field()
    # 所属地区
    ssdq = Field()
    # 所属行业
    sshy = Field()
    # 企业地址
    qydz = Field()
    # 经营范围
    jyfw = Field()
    # 分支机构名称
    fzjgmc = Field()
    # 公司简介
    gsjj = Field()

    # 股东信息
    gdxx = Field()
    # 股东姓名
    # gdxm = Field()
    # 认缴出资额（万元）
    # rjcze = Field()
    # 实缴出资额
    # sjcze = Field()
    # # 认缴出资日期
    # rjczrq = Field()
    # 股东类型
    # gdlx = Field()


    # 主要成员
    zycy = Field()
    # xm = Field()
    # # 姓名
    # zw = Field()
    # # 职务


    # 变更信息
    bgxx = Field()
    # 变更日期
    # bgrq = Field()
    # # 变更前
    # bgq = Field()
    # # 变更后
    # bgh = Field()
    # # 变更项目
    # bgxm = Field()

    # 对外投资
    dwtz = Field()

    # 页面访问网址
    url = Field()
    # 抓取时间
    crawltime = Field()
    # 爬虫名
    spider_name = Field()
    # 来源
    source_domain = Field()

    def get_row_key(self):
        return '%s' % (self['gsmc'])


class RawCorpItemLoader(ItemLoader):
    default_item_class = RawCorpItem
    default_input_processor = MapCompose(lambda s: s.strip())
    default_output_processor = TakeFirst()
    description_out = Join()