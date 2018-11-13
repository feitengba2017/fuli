import scrapy
from random import shuffle
import re
from scrapy.contrib.loader import ItemLoader
from fuli.items import Work28
import time


class Work28Spider(scrapy.Spider):
    name = "work28"
    allowed_domains = ["www.work28.com"]
    start_urls = [
        "https://www.work28.com/category-6.html",
        "https://www.work28.com/category-4.html"
    ]

    def parse(self, response):
        urls = response.xpath('//div[@class="listbody"]//a/@href').extract()
        shuffle(urls)
        pattern = re.compile(r'https://www.work28.com/post/[0-9]{3,7}')
        for url in urls:
            if pattern.search(url):
                req = scrapy.Request(url=url,
                                     callback=self.parse_article,
                                     headers={'Referer': response.url}
                                     )
                yield req

    def parse_article(self, response):
        l = ItemLoader(item=Work28(), response=response)
        l.add_value('spider_name', self.name)
        l.add_xpath('title', '//h1/text()')
        l.add_value('link', response.url)
        l.add_value('datatime', int(time.time()))
        l.add_xpath('content', '//div[@class="article_content"]/node()')
        return l.load_item()