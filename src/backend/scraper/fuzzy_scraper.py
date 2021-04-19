"""
When user gives a incomplete query
(e.g. given"日食", we might want to fill "记"),
we often want to show related suggestions.
However, this requires a big database that we don't have.
Thus we will instead scrape the result 
from search.bilibili.com.
"""
from bs4 import BeautifulSoup
from time import sleep
import re
import sys
import requests

def scrape_related_suggestions(query):
    """
    Given a user query, pass it to search.bilibili database
    and find search suggestions.
    : query : (string) Query from user
    : return : a list of related keywords scraped from search.bilibili.com
    """
    url = f"http://s.search.bilibili.com/main/suggest?func=suggest&suggest_type=accurate&sub_type=tag&main_ver=v1&highlight=&userid=&bangumi_acc_num=1&special_acc_num=1&topic_acc_num=1&upuser_acc_num=3&tag_num=10&special_num=10&bangumi_num=10&upuser_num=3&term={query}&jsonp=jsonp"
    try:
        response = requests.get(url).json()
        results = response["result"]["tag"]
        related_suggestions = []
        for res in results:
            suggestion = res.get("value")
            related_suggestions.append(suggestion)
        return related_suggestions
    except: 
        return []

if __name__ == "__main__":
    print(scrape_related_suggestions("王者荣"))
