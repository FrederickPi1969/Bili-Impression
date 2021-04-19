import requests
import unittest

# !: Activate Server in terminal first, then run the test!
class ServerTests(unittest.TestCase):
    # url template: url_pre + "scraper/comments?keyword=arknights&maxPage=1&maxVideos=5&rankOpt=0&tidOpt=0&sortOpt=1"
    def setUp(self):
        self.url_pre = "http://127.0.0.1:5000/"

    def test_valid_comments_scrape(self):
        url = self.url_pre + "scraper/comments?keyword=arknights&maxPage=1&maxVideos=5&rankOpt=0&tidOpt=0&sortOpt=1"
        res = requests.get(url)
        self.assertEqual(res.status_code, 200)

    def test_invalid_maxPage_comments_scrape(self):
        url = self.url_pre + "scraper/comments?keyword=arknights&maxPage=aaa&maxVideos=5&rankOpt=0&tidOpt=0&sortOpt=1"
        res = requests.get(url)
        self.assertEqual(res.status_code, 400)

    def test_invalid_tidOpt_comments_scrape(self):
        url = self.url_pre + "scraper/comments?keyword=arknights&maxPage=1&maxVideos=5&rankOpt=0&tidOpt=Wrong&sortOpt=1"
        res = requests.get(url)
        self.assertEqual(res.status_code, 400)

    def test_OutBound_sortOpt_comments_scrape(self):
        url = self.url_pre + "scraper/comments?keyword=arknights&maxPage=1&maxVideos=5&rankOpt=0&tidOpt=0&sortOpt=3"
        res = requests.get(url)
        self.assertEqual(res.status_code, 400)

    def test_wrong_route(self):
        url = self.url_pre + "scrapy/comments?keyword=arknights&maxPage=1&maxVideos=5&rankOpt=0&tidOpt=0&sortOpt=3"
        res = requests.get(url)
        self.assertEqual(res.status_code, 404)

    def test_wrong_route2(self):
        url = self.url_pre + "scraper/comments/comments?keyword=arknights&maxPage=1&maxVideos=5" \
                             "&rankOpt=0&tidOpt=0&sortOpt=1"
        res = requests.get(url)
        self.assertEqual(res.status_code, 404)

    def test_empty_option(self):
        url = self.url_pre + "scraper/comments"
        res = requests.get(url)
        self.assertEqual(res.status_code, 400)

    def test_incomplete_option(self):
        url = self.url_pre + "scraper/comments?keyword=arknights&maxPage=1&maxVideos=5&rankOpt=0&tidOpt=0"
        res = requests.get(url)
        self.assertEqual(res.status_code, 400)

    def test_wrong_request_type(self):
        url = self.url_pre + "scraper/comments?keyword=arknights&maxPage=1&maxVideos=5&rankOpt=0&tidOpt=0&sortOpt=1"
        res = requests.post(url)
        self.assertEqual(res.status_code, 405)

    def test_unimplemented_functionality(self):
        url = self.url_pre + "/visualization/wordCloud?keyword=arknights&maxPage=1&maxVideos=5" \
                             "&rankOpt=0&tidOpt=0&sortOpt=1"
        res = requests.get(url)
        self.assertEqual(res.status_code, 400)


if __name__ == '__main__':
    unittest.main()
