# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re

class NavernewsPipeline(object):
    def process_item(self, item, spider):
        # if item['title'] : item['title'] = item['title'].replace('"','')
        # if item['summary'] : item['summary'] = item['summary'].replace('"','')

        cont = ' '.join([item.strip() for item in item['content']  ]) #좌우 공백 제거
        # cont = cont[cont.find('{}')+3:] #javascript 함수 제거
        # cont = re.sub(r"(\(.*\=)|(\[.*\=)|(\[.*\])","",cont) #기자 매체명 삭제
        # cont = cont[:cont.find(r'▶')] #특수문자
        # cont = cont[:cont.find(r'☞')] #특수문자
        # cont = cont[:cont.find(r'ⓒ')] #특수문자
        # cont = cont[:cont.find(r'<ⓒ')] #특수문자
        # cont = re.sub(r"(\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3}))","",cont) #이메일 삭제
        item['content'] = cont
        return item
