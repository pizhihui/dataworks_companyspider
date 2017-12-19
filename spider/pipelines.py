# -*- coding: utf-8 -*-


import hashlib
import datetime
import requests
import logging

class FileWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('company.txt', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        for n in item['name']:
            self.file.write(n.encode("utf-8") + '\n')
        return item


class HBaseItemPipeline(object):
    """  HbasePipeline  """

    # def __init__(self):
    #
    #
    # @classmethod
    # def from_crawler(cls, crawler):
    #     return cls(
    #         test_host=crawler.settings.get('HBASE_TEST_HOST'),
    #         port=crawler.settings.get('HBASE_PORT'),
    #         product_host=crawler.settings.get('HBASE_PRODUCT_HOST')
    #     )

    def open_spider(self, spider):
        self.com_succ = open('company_success.txt', 'w')

    def close_spider(self, spider):
        self.com_succ.close()

    def process_item(self, item, spider):
        if spider.name == "qichabao_com":
            table_name = item.table_name
            row_key = item.get_row_key()
            column_family = item.column_family

            row = hashlib.new("md5", row_key).hexdigest()
            self.com_succ.write("成功写入的公司是: %s %s \n" %(row, item['gsmc']) )
            self.com_succ.flush()
            self.__common_platform_server(item=item, table_name=table_name, row=row)

    def __genMutations(self, item, column_family):
        mutations = {}
        for field in item.fields:
            value = item.get(field)
            if value:
                if isinstance(value, datetime.datetime):
                    value = value.strftime("%Y-%m-%d %H:%M:%S")
                elif isinstance(value, unicode) or isinstance(value, str):
                    value = value.encode('utf-8')
                else:
                    value = str(value)

            column = '%s:%s' % (column_family, field)
            value = value
            mutations[column] = value
        return mutations

    def __common_platform_server(self, item, table_name, row):
        """
        netty的hbase的http服务器接口
        :param item:
        :param table_name:
        :param row:
        :return:
        """
        data_tmp = {}
        for field in item.fields:
            value = item.get(field)
            data_tmp[field] = value
        data = {
            'command': 'put',
            'content': {
                'table': table_name,
                'rowKey': row,
                'family': item.column_family,
                'columnValues': data_tmp,
            }
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
            "Content-Type": "application/json",
            "Connection": "keep-alive",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
        }
        # 10.10.4.168
        requests.post('http://10.10.4.168:8986', json=data, headers=headers)


