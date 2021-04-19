import sys
sys.path.append("./")
import unittest
from src.backend.scraper import fuzzy_scraper as fsp
from bs4 import BeautifulSoup
import requests

class TestFuzzySearchScraper(unittest.TestCase):
    def test_fuzzy_search_common_case(self):
        """
        1. Test fuzzy search scraper can successfully fetch the result
            & decode the Chinese characters correctly.
        """
        related = fsp.scrape_related_suggestions("明日")
        print(related)
        self.assertTrue("明日方舟危机合约" in related)

    def test_fuzzy_search_no_suggestion(self):
        """
        2. Test fuzzy search scraper returns empty list if
            the user query has no related suggestions & program won't crash.
        """
        related = fsp.scrape_related_suggestions("aaksnfnfneksaa")
        self.assertTrue(len(related) == 0)


if __name__ == "__main__":
    unittest.main()


