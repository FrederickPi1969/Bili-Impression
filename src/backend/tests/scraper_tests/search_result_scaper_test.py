import sys
sys.path.append("./")
import unittest
from src.backend.scraper import scraper as scp
from bs4 import BeautifulSoup
import requests

class TestSearchResultVideoScraper(unittest.TestCase):


    def test_result_info_collection_20_videos_common(self):
        """
        1. Test result page info collector can handle common case
            of full load of 20 videos. As the video recommendatoin results/rankings
            vary from time to time, we cannot test with a hard assertion!
        """
        url = "https://search.bilibili.com/all?keyword=%E5%8D%A1%E8%9C%9C%E5%B0%94"
        result_info_dict = scp.extract_video_info_in_search_result_page(url)
        self.assertEqual(len(result_info_dict), 20)

    def test_result_info_collection_20_videos_top_bangumi(self):
        """
        2. Test result page info collector can ignore top area
            bangumis can scrape all wanted videos only.
        """
        url = "https://search.bilibili.com/all?keyword=MegaloBox&from_source=nav_search_new&page=1"
        result_info_dict = scp.extract_video_info_in_search_result_page(url)
        self.assertEqual(len(result_info_dict), 20)

    def test_result_info_collection_less_than_20_videos(self):
        """
        3. Corner case where one page has less than 20 videos.
        """
        url = "https://search.bilibili.com/all?keyword=kkknnn&from_source=nav_search_new&page=1"
        result_info_dict = scp.extract_video_info_in_search_result_page(url)
        self.assertTrue(len(result_info_dict) < 20)


    def test_result_info_collection_empty_results(self):
        """
        4. Make sure program won't crash if user input a query
            that has 0 search results.
        """
        url = "https://search.bilibili.com/all?keyword=asdadadadadadadsadad&from_source=nav_search_new&page=1"
        result_info_dict = scp.extract_video_info_in_search_result_page(url)
        self.assertEqual(len(result_info_dict), 0)


if __name__ == "__main__":
    unittest.main()
 

