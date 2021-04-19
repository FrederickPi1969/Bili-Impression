"""
Bilibili's filtering result is not always satisfying,
i.e. it's quite often that we will see videos that
are irrelevant to our queries.
This module handles aims to check the relevancy of
video result and the query.
"""
from bs4 import BeautifulSoup
from time import sleep
import re
import sys
import requests
from src.backend.scraper.loggers import logger
from src.backend.scraper.dicts.tid_dict import idx2tid
from src.backend.scraper.dicts.rank_order_dict import idx2rank_order


BASE_ROUTE = "https://www.bilibil.com/"

def print_progress(i,  max_len, per=1):
    if (i + 1) % per != 0: return
    print(f"Progress: {i + 1} / {max_len}")

def extract_video_tags(soup):
    """
    Given the html soup of one video of shape https://www.bilibili.com/video/*,
    extract the tags of video.
    """
    try:
        tag_list = soup.select("ul > li.tag")
        tags = []
        for tag_elem in tag_list:
            tags.append(tag_elem.text.strip())
        return tags
    except:
        return []

def extract_video_description(soup):
    """
    Given the html soup of one video of shape https://www.bilibili.com/video/*,
    extract the description of video.
    """
    try:
        desc_wrapper = soup.select("#v_desc > div.info")[0]
        return desc_wrapper.text.strip().replace("\n", " ")
    except:
        return ""

def extract_video_authors(soup):
    """
    Given the html soup of one video of shape https://www.bilibili.com/video/*,
    extract the author of video.
    :return: author dict of format {author_name_[1...n] : author_url[1...n]}
    """

    try:
        up_div = soup.select("#v_upinfo > div.up-info_right > div.name")
        if len(up_div) != 0: # Single UP
            up_div = up_div[0]
            name_a = up_div.find("a", {"class" : re.compile(r"username*")})
            author_name = name_a.text.strip()
            author_url = BASE_ROUTE + name_a["href"][2:]
            return {author_name : author_url}
            
        else: # many UPs
            all_up_divs = soup.select("div.up-card")
            author_dict = {}
            for div in all_up_divs:
                author_div = div.find("div", "avatar-name__container")
                author_url = BASE_ROUTE +  author_div.a["href"][2:] # first two char are "//"
                author_name = author_div.text.strip()
                author_dict[author_name] = author_url
            return author_dict

    except:
        return {}


def extract_video_title(soup):
    try:
        video_title_meta = soup.find(name='h1', attrs={'class': 'video-title'})
        video_title = video_title_meta["title"].strip()
        return video_title
    except:
        return ""

def extract_video_oid(html):
    """
    Given the src html (not soup)!
    of one video of shape https://www.bilibili.com/video/*,
    extract the oid (aka upgcxcode) of video.
    """
    try:
        locator = html.index("upgcxcode")
        oid_info = html[locator:locator+50] 
        oid = re.findall(r"upgcxcode/[0-9]{1,3}/[0-9]{1,3}/([0-9]*?)/", oid_info)[0]
        return oid 
    except:
        return None

def extract_video_av(soup):
    """
    Given the html soup of one video of shape https://www.bilibili.com/video/*,
    extract the AV number of video.
    """
    try:
        comment_meta = soup.find(name='meta', attrs={'itemprop': 'url'}) # find the one in header
        video_url = comment_meta["content"]
        av = re.findall(r"^https://www.bilibili.com/video/av([0-9]+)/$", video_url)[0]
        return av
    except:
        return None

def judge_is_video_related(keyword, tags, description, author_dict, video_title):
    """
    ASSUMPTIONS: 
    1. semantic units in keyword are separated with
       empty spaces by users. e.g. "碧蓝航线 柴郡"
    2. There are no punctuations or other special tokens in the keyword,
       otherwise they will be treated as part of exact matches.
    Judge whether one video is relevant to the query keyword.
    :return: True if judged as related, False otherwise
    """
    semantic_units = keyword.split(" ")
    tags = [tag.lower() for tag in tags] # case insensitive
    description = description.lower()
    authors = [author.lower() for author in author_dict.keys()]
    title = video_title.lower()
    for unit in semantic_units:
        unit = unit.lower()
        contained_in_tags = any([unit in tag for tag in tags])
        contained_in_authors = any([unit in author for author in authors])
        contained_in_desc = unit in description
        contained_in_title = unit in title
        if not contained_in_tags and not contained_in_authors\
            and not contained_in_desc and not contained_in_title:
            return False
    return True

def retrive_relevant_videos_info(keyword, candidates):
    """
    Given a list of candidate videos urls,
    first judge whether each of them is relevant
    to query key based on video tags, descriptions & author info.
    Then extract av, oid, description, tags, title of relevant video,
    and return as a dict (bv as key).
    :return: a dictionary containing many video_url-value pairs of
    {video_bv[1...n] : {av->str, oid->str, author_info->dict(name: url),
            tags->list, desc->str}}
    """
    print("\n\n----------------------------------------------------------")
    logger.info("Retriving candidate video information and filtering...\n\n")
    filtered_video_info = {}
    for i, url in enumerate(candidates):
        bv = re.findall(r"^https://www.bilibili.com/video/BV([0-9a-zA-Z]*).*$", url)[0]
        src_html = requests.get(url).text
        soup = BeautifulSoup(src_html, "lxml")
        print_progress(i, len(candidates), per=5)
        author_dict = extract_video_authors(soup)
        tags = extract_video_tags(soup)
        description = extract_video_description(soup)
        video_title = extract_video_title(soup)
        # only extract av and oid for relevant videos
        
        if judge_is_video_related(keyword, tags, description, author_dict, video_title):
            oid = extract_video_oid(src_html)
            av = extract_video_av(soup)
            if oid is None or av is None:
                continue  # ignore videos whose av or oid are not found
            filtered_video_info[bv] = {
                "av": av,
                "oid": oid,
                "tags": tags,
                "description": description,
                "title": video_title
            } 

    return filtered_video_info
        
                
if __name__ == "__main__": 
    print(retrive_relevant_videos_info("原子Dan 音乐", ["https://www.bilibili.com/video/BV1Fh411C791"]))
    
    

