# coding=utf-8
from elasticsearch import Elasticsearch
import json
import os
import time




def main():

    es = Elasticsearch('10.10.4.148:9200')
    index = 'corp_index'
    table_name = 'raw_corp'
    # 判断是否创建了
    if es.indices.exists(index=index) is not True:
        #es.indices.create(index='blog_index', body=_index_mappings)
        es.indices.create(index=index)
    # 判断是否创建了doc_type,没有的话创建doc_type及mapping
    if es.indices.exists_type(index=index, doc_type=table_name) is not True:
        #file_path = os.getcwd() + '/spider/mapping/mapping_' + table_name + '_test.json'
        print os.getcwd()
        file_path = os.getcwd() + '/mapping/mapping_' + table_name + '.json'
        file_obj = open(file_path)
        try:
            all_content = file_obj.read()
            #print all_content
            es.indices.put_mapping(index=index, doc_type=table_name, body=all_content, update_all_types=True)
        except BaseException, e:
            print e
        finally:
            file_obj.close()


if __name__=="__main__":
    main()