import scrapy
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join
from fuli.tools import common


class Work28(scrapy.Item):
    spider_name = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field(
        input_processor=MapCompose(common.get_md5)
    )
    datatime = scrapy.Field()
    content = scrapy.Field()
