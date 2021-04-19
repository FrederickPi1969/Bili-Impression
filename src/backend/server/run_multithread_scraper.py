from src.backend.scraper.multi_thread_scraper import start_scraping
from threading import Thread, Lock
import json
import random
from src.backend.server.proxy_validator import proxy_validation
from bson import json_util
import time

# used for testing and presentation
if __name__ == "__main__":
    start = time.time()
    result = start_scraping("arknights", max_page=50, max_videos=1, max_proxy=50)
    print(result)
    with open('search result.txt', 'w') as search_result:
        json.dump(result[0], search_result, default=json_util.default)
    with open('candidate.txt', 'w') as candidate:
        json.dump(result[1], candidate)
    elapsed = time.time() - start
    print(f"finished!, totally used {elapsed} seconds.")






