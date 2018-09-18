# -*- coding: utf-8 -*-
import scrapy

import os

from scrapy_redis.spiders import RedisSpider

from Sina.items import SinaItem


class SinaGuideSpider(RedisSpider):
    name = 'sina_guide'

    # redis_key，唯一
    redis_key = 'sinaguidespider:start_urls'
    # 别写错了
    allowed_domains = ['sina.com.cn']

    start_urls = ['http://news.sina.com.cn/guide/']

    # 爬取帖子的内容
    def detail_tiezi(self, response):
        item = response.meta["item"]

        # 帖子的链接
        tiezi_url = response.url

        # 帖子的标题
        tiezi_title = response.xpath('//h1[@id="artibodyTitle"]/text()|//h1[@class="main-title"]/text()').extract()
        if tiezi_title:
            tiezi_title = tiezi_title[0]

        # 帖子内容
        tiezi_content = response.xpath('//div[@class="article"]//p//text()|//div[@id="artibody"]//p//text()').extract()

        if tiezi_content:
            tiezi_content = "".join(tiezi_content)

        item["tiezi_title"] = tiezi_title
        item["tiezi_url"] = tiezi_url
        item["tiezi_content"] = tiezi_content

        print("---------------------------------")
        print("item==", item)
        print("reponse.url==", response.url)

        yield item

    # 得到所有帖子的链接
    def seconde_detail(self, response):
        # print("seconde_detail reponse.url==", response.url)

        # item对象
        item = response.meta["item"]
        # print("item==", item)
        urls = response.xpath('//a/@href').extract()

        parent_url = item["parent_url"]

        for url in urls:

            # 当前页所有连接，有些是不是我们要抓取
            if url.startswith(parent_url) and url.endswith(".shtml"):
                yield scrapy.Request(url, callback=self.detail_tiezi, meta={"item": item})

    def parse(self, response):
        # print("reponse.url==",response.url)

        # 大标题：parent_title
        parent_titles = response.xpath('//div[@id="tab01"]//h3[@class="tit02"]/a/text()').extract()
        # 大标题的链接：parent_url
        parent_urls = response.xpath('//div[@id="tab01"]//h3[@class="tit02"]/a/@href').extract()
        # 小标题：sub_title
        sub_titles = response.xpath('//div[@id="tab01"]//ul[@class="list01"]/li/a/text()').extract()
        # 小标题的链接：sub_url
        sub_urls = response.xpath('//div[@id="tab01"]//ul[@class="list01"]/li/a/@href').extract()

        print(len(parent_titles), len(parent_urls))
        print(len(sub_titles), len(sub_urls))

        # 大标题
        for index in range(len(parent_titles)):

            parent_title = parent_titles[index]

            parent_url = parent_urls[index]

            # print("parent_title==",parent_title,"parent_url==",parent_url)

            # 循环小标题
            for index_sub in range(len(sub_urls)):

                sub_title = sub_titles[index_sub]

                sub_url = sub_urls[index_sub]

                # https://news.sina.com.cn/   新闻
                # https://news.sina.com.cn/china/ 国内
                if sub_url.startswith(parent_url):
                    # print("sub_title==",sub_title,"sub_url==",sub_url,"parent_url==",parent_url)

                    sub_path = "./datas/" + parent_title + "/" + sub_title

                    if not os.path.exists(sub_path):
                        os.makedirs(sub_path)

                    # 这个item没有完整，携带到下一个请求，成功后再把数据补上

                    item = SinaItem()

                    item["parent_title"] = parent_title
                    item["parent_url"] = parent_url
                    item["sub_title"] = sub_title
                    item["sub_url"] = sub_url
                    item["tiezi_path"] = sub_path

                    # 直接请求
                    yield scrapy.Request(sub_url, callback=self.seconde_detail, meta={"item": item})
