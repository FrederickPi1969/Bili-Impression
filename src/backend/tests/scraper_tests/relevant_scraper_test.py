import sys
sys.path.append("./")
import unittest
from src.backend.scraper import relevant_scraper as rs
from bs4 import BeautifulSoup
import requests

class TestRelevantScraper(unittest.TestCase):
    def test_case_keyword_contained_in_title(self):
        """
        0. Case where keyword is only contained in title.
        The video should be judged as relevant.
        """
        keyword = "宫保鸡丁"
        video_url = "https://www.bilibili.com/video/BV1HW411H7Nj"
        result = rs.retrive_relevant_videos_info(keyword, [video_url])
        self.assertTrue(len(result) == 1)

    def test_case_keyword_contained_in_uploader_name(self):
        """
        1. Case where keyword is only contained in uploader.
        The video should be judged as relevant.
        """
        keyword = "老番茄"
        video_url = "https://www.bilibili.com/video/BV1m7411X77o"
        result =  rs.retrive_relevant_videos_info(keyword, [video_url])
        self.assertTrue(len(result) == 1)

    def test_case_keyword_contained_in_description(self):
        """
        2. Case where keyword is only contained in video description
        The video should be judged as relevant.
        """
        keyword = "爆地魔"
        video_url = "https://www.bilibili.com/video/BV1ji4y1t7nL"
        result =  rs.retrive_relevant_videos_info(keyword, [video_url])
        self.assertTrue(len(result) == 1)

    def test_case_keyword_contained_in_tags(self):
        """
        3. Case where keyword is only contained in video tags.
        The video should be judged as relevant.
        """
        keyword = "手机游戏"
        video_url = "https://www.bilibili.com/video/BV1iK411774p"
        result =  rs.retrive_relevant_videos_info(keyword, [video_url])
        self.assertTrue(len(result) == 1)


    def test_case_keyword_contained_in_nowhere(self):
        """
        4. Case where keyword is not contained in anywhere.
        The video should be judged as irrelevant.
        """
        keyword = "阿拉斯加"
        video_url = "https://www.bilibili.com/video/BV1Sx411S7Kt"
        result =  rs.retrive_relevant_videos_info(keyword, [video_url])
        self.assertTrue(len(result) == 0)

    def test_case_keyword_2_semantic_units(self):
        """
        5. Case where user provide a keyword containing two semantic units.
        e.g. "绵羊料理 美食"
        Provided a relevant video, test functinoality of judger.
        """
        keyword = "原子Dan 音乐"
        video_url = "https://www.bilibili.com/video/BV1Fh411C791"
        result =  rs.retrive_relevant_videos_info(keyword, [video_url])
        self.assertTrue(len(result) == 1)

    def test_case_keyword_3_semantic_units(self):
        """
        6. Case where user provide a keyword containing three semantic units.
        e.g. "初音 日本 演唱会"
        Provided a relevant video, test functinoality of judger.
        """
        keyword = "初音 日本 演唱会"
        video_url = "https://www.bilibili.com/video/BV1UZ4y1u7jb"
        result =  rs.retrive_relevant_videos_info(keyword, [video_url])
        self.assertTrue(len(result) == 1)

if __name__ == "__main__":
    unittest.main()


