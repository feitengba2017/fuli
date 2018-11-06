import scrapy


class Work28Spider(scrapy.Spider):
    name = "work28"
    allowed_domains = ["https://www.work28.com/"]
    start_urls = [
        "https://www.work28.com/category-6.html",
        "https://www.work28.com/category-4.html"
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2]
        with open(filename, 'wb') as f:
            f.write(response.body)