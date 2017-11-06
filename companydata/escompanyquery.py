#coding:utf-8
import sys
import hashlib
import requests
import json
reload(sys)
sys.setdefaultencoding('utf-8')


from elasticsearch import Elasticsearch

def main():

    outFile = open('escompany.txt', 'w')
    needed = open('esneeded.txt', 'w')

    nettyHeader = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Length": "55",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    }

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


if __name__=="__main__":
    main()