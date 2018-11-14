import scrapy
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join,Identity
from scrapy.contrib.loader import ItemLoader
from fuli.tools import common
from fuli.cleaner.work28 import Work28Extractor


class ArticleItemLoader(ItemLoader):
    # 自定义itemloader,取列表中第一个
    default_output_processor = TakeFirst()

class Work28(scrapy.Item):
    spider_name = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field(
        input_processor=MapCompose(common.get_md5)
    )
    url = scrapy.Field()
    datatime = scrapy.Field()
    content = scrapy.Field(
        input_processor=MapCompose(Work28Extractor.parse_article_content)
    )
