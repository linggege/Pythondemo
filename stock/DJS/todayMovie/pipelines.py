# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import time

class TodaymoviePipeline(object):
    def process_item(self, item, spider):
        return item
        # today = time.strftime('%Y-%m-%d', time.localtime())
        # fileName = '数据' + today + '.txt'
        # with codecs.open(fileName, 'a+', 'utf-8') as fp:
        #     # fp.write('%s %s %s %s \r\n' % (item['movieTitleCn'],
        #     #       item['movieTitleEn'],
        #     #       item['director'],
        #     #       item['runtime']))
        #     fp.write('%s \r\n' % (item['yclr']))
