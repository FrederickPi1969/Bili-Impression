import unittest
import src.backend.server.proxy as Proxy
import src.backend.server.proxy_validator as Validator
import src.backend.server.multithread_proxy_getter as Getter
import time
import src.backend.scraper.multi_thread_scraper as Scraper2
from threading import Thread, Lock


class MultithreadScrapingTests(unittest.TestCase):
    def test_multithread_scraping(self):
        try:
            result = Scraper2.start_scraping("arknights", max_page=5, max_videos=1, max_proxy=50)
            self.assertNotEqual(result, ({},{}))
        except:
            print('failed to execute multithread scraping')
            self.assertFalse(True)

    def test_no_usable_proxy(self):
        try:
            result = Scraper2.start_scraping("arknights", max_page=5, max_videos=1, max_proxy=0)
            self.assertEqual(result, ({},{}))
        except:
            print('failed to execute multithread scraping')
            self.assertFalse(True)