# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

import os

# 自定义Pipeline
from datetime import datetime


class ExamplePipeline(object):

    # 第三个参数是：爬虫MyCrawler类的实例
    def process_item(self, item, spider):
        # 添加爬取时间
        item["crawled"] = datetime.utcnow()
        # 添加爬虫的名称：myspider_redis+"windows_afu"
        item["spider"] = spider.name + "__windows_ZhangWenFeng"
        return item


class SinaTextSavePipeline(object):

    # 保存帖子的内容到文件里面
    def process_item(self, item, spider):
        tiezi_content = item["tiezi_content"]
        tiezi_url = item["tiezi_url"]
        tiezi_path = item["tiezi_path"]

        # http://news.sina.com.cn/pl/2015-08-27/080832240833.shtml -->news_sina_com.cn_pl_2015-08-27_080832240833.txt
        name = tiezi_url[7:tiezi_url.rfind(".")].replace(".", "_").replace("/", "_")

        # ./datas/体育/NBA+"/"+news_sina_com.cn_pl_2015-08-27_080832240833.txt
        file_name = tiezi_path + "/" + name + ".txt"

        if not os.path.exists(file_name):
            with open(file_name, 'w', encoding="utf-8") as f:
                f.write(tiezi_content)

        return item


class SinaPipeline(object):
    def open_spider(self, spider):
        self.file = open("新浪.json", "w", encoding="utf-8")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        self.file.write(json.dumps(dict(item), ensure_ascii=False) + "\n")

        return item
