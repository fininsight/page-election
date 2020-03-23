# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import CsvItemExporter

class CommentCrawlerPipeline(object):
    def open_spider(self, spider):
        self.comment_exporter = {}
        self.name = spider.name

    def close_spider(self, spider):
        for exporter in self.comment_exporter.values():
            exporter.finish_exporting()
        self.f.close()

    def _exporter_for_item(self, item):
        date = item['date']
        category1 = item['category1']
        category2 = item['category2']
        filename = '{}_{}_{}'.format(date, category1, category2)

        if filename not in self.comment_exporter:
            self.f = open('{}/{}/{}/{}/{}.csv'.format(self.name, date[:4], date[4:6], date[6:], filename), 'wb')
            exporter = CsvItemExporter(self.f, encoding='utf-8')
            exporter.start_exporting()
            self.comment_exporter[filename] = exporter
        return self.comment_exporter[filename]

    def process_item(self, item, spider):
        exporter = self._exporter_for_item(item)
        exporter.export_item(item)
        return item
