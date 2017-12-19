#coding:utf-8
import sys
import hashlib
import requests
import json
import os

reload(sys)
sys.setdefaultencoding('utf-8')


from elasticsearch import Elasticsearch

nettyHeader = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Length": "55",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    }

def main():

    outFile = open('escompany.txt', 'w')
    needed = open('esneeded.txt', 'w')



    es = Elasticsearch('10.10.4.148:9200')
    _query_name_contains = {
      'query': {
        'match': {
          'ent_name_kw': '*'
        }
      }
    }
    query_all = {
        "query": {
         "match_all": {}
        },
        "collapse": {
            "field": "ent_name_kw"
          },
        "size": 10000,
        #"from": 3
    }
    res = es.search(index='cia_index',
                    doc_type=['raw_fin_bids', 'raw_fin_info'],
                    body=query_all,
                    filter_path=['hits.hits._source.ent_name_kw'])

    for val in res['hits']['hits']:
        v = val['_source']['ent_name_kw']
        print v
        outFile.write(str(v.encode('utf-8')) + '\n')
    print res

    for val in res['hits']['hits']:
        tmp_com_name = val['_source']['ent_name_kw']
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
        res = requests.post('http://10.10.4.158:8986', json=data, headers=nettyHeader)
        if not json.loads(res.content)['result']:
            needed.write(tmp_com_name + '\n')

    needed.close()
    outFile.close()

def hbase_query():
    file_path_trg = os.getcwd() + "/allcompanydata_new.txt"
    file_path_needed = os.getcwd() + "/company_last.txt"

    file_needed = open(file_path_needed, 'w')

    with open(file_path_trg, 'r') as f:
        companys = f.readlines()
        for com in companys:
            row_key = hashlib.new("md5", com.strip().replace('\n','')).hexdigest()
            data = {
                "command": "getByRowKey",
                "content": {
                    "table": "raw_corp",
                    "rowKey": row_key,
                    "family": "info"
                }
            }
            res = requests.post('http://10.10.4.158:8986', json=data, headers=nettyHeader)
            if not json.loads(res.content)['result']:
                file_needed.write(com)

    file_needed.close()

if __name__=="__main__":
    hbase_query()