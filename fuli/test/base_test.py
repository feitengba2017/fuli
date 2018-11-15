import unittest
import os
from scrapy.http import HtmlResponse, Request


class BaseTest(unittest.TestCase):

    def local_repsonse(self, text, url=None):
        if not url:
            url = 'http://www.example.com'

        request = Request(url=url)
        if not text[0] == '/':
            responses_dir = os.path.dirname(os.path.realpath(__file__))
            file_path = os.path.join(responses_dir, text)
        else:
            file_path = text

        file_content = open(file_path, 'r').read()
        response = HtmlResponse(url=url, request=request, body=file_content)
        return response
