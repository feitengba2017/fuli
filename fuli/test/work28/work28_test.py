import unittest
from ..base_test import BaseTest
from fuli.cleaner.work28 import Work28Extractor
import json


class Work28Test(BaseTest):

    def setUp(self):
        self.extractor = Work28Extractor()

    def test(self):
        url = ('')
        resp = self.local_repsonse('work28/test_page.html', url)
        item = self.extractor.process_item(resp)
        print(item)
        self.assertTrue(item['content'])
        self.assertTrue(False)
        '''nosetests fuli.test.work28.work28_test:Work28Test'''

if __name__ == '__main__':
    unittest.testmod()
