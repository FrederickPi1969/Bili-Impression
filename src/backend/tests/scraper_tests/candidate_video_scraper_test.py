import sys
sys.path.append("./")
import unittest
from bs4 import BeautifulSoup
import requests
from src.backend.scraper import relevant_scraper as rs
from src.backend.scraper.scraper import extract_danmaku, extract_info_from_video_comments

class TestCandidateVideoScraper(unittest.TestCase):
    
    def test_scrape_single_author(self):
        """
        1. Collect authors for cases where a candidate video has a single author.
        """
        url = "https://www.bilibili.com/video/BV1xx411c7mu?from=search&seid=7295873980853754728"
        res = requests.get(url).text
        soup = BeautifulSoup(res, "lxml")
        author_dict = rs.extract_video_authors(soup)
        self.assertEqual(list(author_dict.keys())[0], "TSA");
        


    def test_scrape_multiple_authors(self):
        """
        2. Collect authors for cases where a candidate video has multiple authors.
        """
        url = "https://www.bilibili.com/video/BV1wE411y72h"
        res = requests.get(url).text
        soup = BeautifulSoup(res, "lxml")
        author_dict = rs.extract_video_authors(soup)
        self.assertEqual(len(author_dict.keys()), 7)

    def test_scrape_early_video_av(self):
        """
        3. Test av of a video published in 2009 can be retrived.
        """
        url = "https://www.bilibili.com/video/av2"
        res = requests.get(url).text
        soup = BeautifulSoup(res, "lxml")
        av = rs.extract_video_av(soup)
        self.assertEqual(av, "2")

    def test_scrape_recent_video_av(self):
        """
        4. Test av of a video published at 04/04/2021 can be retrived.
        """
        url = "https://www.bilibili.com/video/BV1of4y1x7cv"
        res = requests.get(url).text
        soup = BeautifulSoup(res, "lxml")
        av = rs.extract_video_av(soup)
        self.assertEqual(av, "289923115")


    def test_scrape_invalid_av(self):
        """
        5. Case where a video has been deleted or does not exist.
        """
        url = "https://m.bilibili.com/video/BVpmsdfsifsifsifsfbsibfsbfsf"
        res = requests.get(url).text
        soup = BeautifulSoup(res, "lxml")
        av = rs.extract_video_av(soup)
        self.assertIsNone(av)

    def test_scrape_video_title(self):
        """
        6. Test title of videos can be correctly retrived.
            Notice that every video has a mandatory title on Bilibili.
        """
        url = "https://m.bilibili.com/video/BV1Qt411T7VS"
        res = requests.get(url).text
        soup = BeautifulSoup(res, "lxml")
        title = rs.extract_video_title(soup)
        self.assertEqual(title.replace(" ", ""), "影流之主")

    def test_scrape_video_description(self):
        """
        7. Test description of videos can be correctly retrived.
            Notice that every video has a mandatory description.
        """
        url = "https://www.bilibili.com/video/BV1ns411s7Fq"
        res = requests.get(url).text
        soup = BeautifulSoup(res, "lxml")
        desc = rs.extract_video_description(soup)
        truth = "38—40期图包+曲包：http://pan.baidu.com/s/1bYcoVk"
        self.assertEqual(desc, truth)

    def test_scrape_video_tags(self):
        """
        8. Test tags of videos can be correctly retrived.
            Notice that every video has at least on tag.
        """
        url = "https://www.bilibili.com/video/BV1rK4y1J7hJ"
        res = requests.get(url).text
        soup = BeautifulSoup(res, "lxml")
        tags = rs.extract_video_tags(soup)
        self.assertTrue("原神" in tags)
        self.assertTrue("手机游戏" in tags)
        self.assertTrue("圣遗物" in tags)

    def test_scrape_video_oid(self):
        """
        9. Test oid of videos can be correctly retrieved.
        """
        url = "https://www.bilibili.com/video/BV1Dp4y1H7RE"
        res = requests.get(url).text
        oid = rs.extract_video_oid(res)
        self.assertTrue(oid, "309517865")

    def test_scrape_invalid_video_oid(self):
        """
        10. Test oid of invalid videos won't cause run time error and return None.
        """
        url = "https://www.bilibili.com/video/BV1Dp4y1H7REkldoiajjdoads"
        res = requests.get(url).text
        oid = rs.extract_video_oid(res)
        self.assertIsNone(oid)

    def test_relavant_video_pipeline_valid_case(self):
        """
        11. Test the whether the pipeline of
            video-info-extraction, video-filtering, data-wrapping pipeline
            can be done correctly on a video in good shape & good match (week 1).
        """
        url = ["https://www.bilibili.com/video/BV16v4y1o75c"]
        video_info_dicts = rs.retrive_relevant_videos_info("埃尔梅罗Ⅱ世事件簿", url)
        self.assertEqual(video_info_dicts["16v4y1o75c"]["av"], "544009498")
        self.assertEqual(video_info_dicts["16v4y1o75c"]["oid"], "295524166")
        self.assertTrue("格蕾" in video_info_dicts["16v4y1o75c"]["tags"])

    def test_relavant_video_pipeline_invalid_case(self):
        """
        12. Suppose the av/oid of video is non-retrivable because video does not exist,
            make sure the pipeline still runs without error.
        """
        url = ["https://www.bilibili.com/video/BV16v4y1o75caaa"]
        video_info_dicts = rs.retrive_relevant_videos_info("埃尔梅罗Ⅱ世事件簿", url)
        self.assertTrue("16v4y1o75caaa" not in video_info_dicts)

    def test_danmaku_retrival(self):
        """
        13. Test that given a valid oid, the scraper can retrive danmaku of the video.
        """
        oid = "309517865"
        damakus = extract_danmaku(oid)
        self.assertTrue(len(damakus) > 0)


    def test_comments_and_sex_retrival(self):
        """
        14. Given a valid av, the scraper can retrive comments of the video.
        """
        av = "2"
        sex_list, comments = extract_info_from_video_comments(av)
        self.assertTrue(len(sex_list) > 0)
        self.assertTrue(len(comments) > 0)

if __name__ == "__main__":
    unittest.main()
 

