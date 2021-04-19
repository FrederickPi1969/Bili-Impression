import sys
sys.path.append("./")
import unittest
from src.backend.scraper import scraper as scp
from bs4 import BeautifulSoup
import requests

class TestScraperInterface(unittest.TestCase):
    def test_no_second_hand_rank(self):
        """
        1. Test the most the upper-level scraper interface can run
        with no second-hand ranking requirement.
        """
        keyword = "刺客"
        search_result_info, candidate_info = \
            scp.start_scraping(keyword, max_pages=1, max_videos=1, sort_option="0")
        self.assertTrue(len(search_result_info) == 20, len(candidate_info) == 1)

    def test_second_hand_rank_with_view_count(self):
        """
        2. Test the most the upper-level scraper interface can run
        with second-hand ranking requirement as total view count.
        """
        keyword = "原神"
        search_result_info, candidate_info = \
            scp.start_scraping(keyword, max_pages=1, max_videos=1, sort_option="1")
        self.assertTrue(len(search_result_info) == 20, len(candidate_info) == 1)

    def test_second_hand_rank_with_time(self):
        """
        3. Test the most the upper-level scraper interface can run
        with second-hand ranking requirement as most recent update.
        """
        keyword = "美食作家王刚"
        search_result_info, candidate_info = \
            scp.start_scraping(keyword, max_pages=1, max_videos=1, sort_option="2")
        self.assertTrue(len(search_result_info) == 20, len(candidate_info) == 1)


if __name__ == "__main__":
    unittest.main()


