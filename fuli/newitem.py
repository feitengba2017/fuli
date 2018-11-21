import scrapy

class NewsItem(scrapy.Item):
    content = scrapy.Field()
    img_src = scrapy.Field()
    video_src = scrapy.Field()
    script_src = scrapy.Field()
    embed_html = scrapy.Field()