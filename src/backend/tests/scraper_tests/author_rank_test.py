import sys
sys.path.append("./")
import unittest
from bs4 import BeautifulSoup
import requests
import pickle as pkl
from src.backend.author_ranker import ranker

class TestAuthorRanker(unittest.TestCase):
    def test_naive_ranking(self):
        """
        1. Test naive ranking algorithm can run without error.
        """
        with open ("./美食.pkl", "rb") as file:
            search_result_video_info = pkl.load(file)
        result = ranker.find_top_k_authors(search_result_video_info, 25, corrected=False)
        assert(len(result) == 25)

    def test_enhanced_ranking(self):
        """
        2. Test video-weight enhanced ranking algorithm can run without error.
        """
        with open ("./美食.pkl", "rb") as file:
            search_result_video_info = pkl.load(file)
        result = ranker.find_top_k_authors(search_result_video_info, 30,  corrected=True)
        assert(len(result) == 30)

if __name__ == "__main__":
    unittest.main()


