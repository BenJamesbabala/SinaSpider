# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SinaItem(scrapy.Item):
    # 大标题：parent_title
    parent_title = scrapy.Field()
    # 大标题的链接：parent_url
    parent_url = scrapy.Field()

    # 小标题：sub_title
    sub_title = scrapy.Field()
    # 小标题的链接：sub_url
    sub_url = scrapy.Field()




    # 帖子存放的路径: tiezi_path
    tiezi_path = scrapy.Field()

    # 帖子的ulr: tiezi_url
    tiezi_url = scrapy.Field()

    # 帖子的标题：tiezi_title
    tiezi_title = scrapy.Field()
    # 帖子的内容：tiezi_content
    tiezi_content = scrapy.Field()
    #爬取的时间
    crawled = scrapy.Field()

    #爬虫的名称
    spider = scrapy.Field()
