"""
This module handles the basic scraping functionalities,
including collecting videos av&oid, tags, danmaku, comments,
commenters, user's followings.
"""
from bs4 import BeautifulSoup
from time import sleep
import re
import sys
import requests
import numpy as np
import datetime
from src.backend.scraper.loggers import logger
from src.backend.scraper.dicts.tid_dict import idx2tid
from src.backend.scraper.dicts.rank_order_dict import idx2rank_order
from src.backend.scraper.relevant_scraper import retrive_relevant_videos_info
from src.backend. scraper.video_rank import *
import pickle as pkl
import time

BASE_ROUTE = "https://www.bilibil.com/"

def print_progress(i,  max_len, per=1):
    if (i + 1) % per != 0: return
    print(f"Progress: {i + 1} / {max_len}")


def construct_page_requests(key, max_pages, rank, tid):
    """
    Given the basic key, page, tid
    information, construct all page requests for getting candidate videos.
    Notice we will use default ranking because it gives best relevancy.
    i.e. page 1 - max_pages urls.
    """
    template = lambda i : f"https://search.bilibili.com/all?keyword={key}&from_source=nav_search_new&order={rank}&duration=0&tids_1={tid}&page={i}"
    return [template(i) for i in range(1, max_pages+1)]


def normalize_view_count(raw_view_count):
    """
    Convert raw view count e.g. 54.2万 to numeric value 542000
    """
    if "万" in raw_view_count:
        review_count = float(raw_view_count.replace("万", "")) * 1e4
        rand_num = np.random.rand() * 1e3 # add a random number for tie breaking.
        return review_count + rand_num
    else:
        return float(raw_view_count) 

def normalize_datetime(raw_date_time):
    """
    Convert raw date time e.g. 2015-2-61 to
    python datetime object for later calculation.
    """
    return datetime.datetime(*[int(s) for s in raw_date_time.split("-")])


def extract_video_info_in_search_result_page(page_request): 
    """
    extract urls, publication date, author, author url
    of videos in one search result page, then return them as dict
    :return: a dict of video information (as stated above).
        format: {video_bv: {up:~, up_url:~, view_count:~, date:~}} 
    TODO: error checking for empty pages!!
    """
    try:
        src_html = requests.get(page_request).text
        soup = BeautifulSoup(src_html, "lxml")
        video_li_list = soup.select("ul.video-list.clearfix > li")
        video_dict = {}
        for video_li in video_li_list:
            video_headline = video_li.find("div", attrs={"class": "headline clearfix"})
            video_url = "https:" + video_headline.a["href"]
            bv = re.findall(r"^https://www.bilibili.com/video/BV([0-9a-zA-Z]*).*$", video_url)[0]        
            video_info = video_li.find("div", attrs={"class": "tags"})
            raw_view_count = video_info.find("span", attrs={"title": "观看"}).text.strip()
            view_count = normalize_view_count(raw_view_count)
            raw_upload_time = video_info.find("span", attrs={"title": "上传时间"}).text.strip()
            upload_time = normalize_datetime(raw_upload_time)
            up_span = video_info.find("span", attrs={"title": "up主"})
            up_info_wrapper = up_span.find("a")
            up_name = up_info_wrapper.text.strip()
            up_url = BASE_ROUTE + up_info_wrapper["href"][2:]
            video_dict[bv] = {
                    "view_count": view_count, "upload_date": upload_time,
                    "author": {up_name : up_url}, "video_url": video_url
                }
        return video_dict
    except:
        return {}
        

def extract_danmaku(oid):
    """
    Given oid of one video, get the video's default shown danmaku
    :param oid: oid of a video extracted previously
    :return:  a list of danmaku of this video  
    """
    try: 
        danmaku_url = f"https://api.bilibili.com/x/v1/dm/list.so?oid={oid}"
        src_xml = requests.get(danmaku_url, "xml").content 

    except:
        return []
    
    parser = BeautifulSoup(src_xml, "lxml") 
    danmaku = [elem.text for elem in parser.select("d")] 
    return danmaku



def extract_info_from_video_comments(av):
    """
    Given oid of one video, get sex distribution of commenters & all comments of the video.
    : av : av identifier of video.
    : return :  sex_list - a list of sex of all commenters
                comment_list - a list of all comments
    """
    sex_list = []
    reply_list = []
    try:
        # maximum result per page is 49 (ps), sorting = 2 (热度排), pn 页数
        comment_url = f"https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn={1}&type=1&oid={av}&ps={49}&sort={2}"
        response = requests.get(comment_url).json()
        replies = response["data"]["replies"]
        for reply_thread in replies:
            # each single reply thread contains child replie
            parent_msg = reply_thread["content"]["message"]
            reply_list.append(parent_msg)
            sex_list.append(reply_thread["member"]["sex"])
            children_replies = reply_thread.get("replies")
            children_replies = children_replies if children_replies is not None else []
            for child_reply in children_replies:
                child_msg = child_reply["content"]["message"]
                reply_list.append(child_msg)
                sex_list.append(child_reply["member"]["sex"])
        return sex_list, reply_list
    except:
        return sex_list, reply_list


def start_scraping(keyword, max_pages=1, max_videos=50, rank_option="0", tid_option="0", sort_option="1"):
    """
    :param keyword: queried topic word
    :param max_pages: maximum page of results to be considered
    :param max_videos: maximum number of videos whose comments & danmaku will be considered
    :param rank_option: the way of ranking videos by Bilibili.com.
                        "0" : "totalrank", "1" : "click", "2" : "pubdate", "3" : "danmaku", "4" : "stow"
    :param tid_option: subarea to be used - anime, food, entertainment, etc.
                        See dir dicts for details.
    :param sort_option: second-hand ranking to be used. "0" for no second-hand-sort,
                        "1" for view-count sort, "2" for upload-date sort.
    Notice all of the above parameters are expected to be passed
    in raw index format. Conversion to url param will be covered 
    in this function.
    :all video info: in search result pages
    """
    tid = idx2tid[tid_option]
    rank = idx2rank_order[rank_option]
    all_page_requests = construct_page_requests(keyword, max_pages, rank, tid)
    search_result_video_info = {}  # all video info, 1000 = 50 pages * 20 per, bv as key
    candidate_video_info = {} # top 50-80 video info, bv as key
        
    # Collect all videos (usually 1000) information in search results pages (50)
    print("\n\n----------------------------------------------------------")
    logger.info("Collecting all videos' information from search results...")
    for i, page_request in enumerate(all_page_requests):  
        print_progress(i, len(all_page_requests))
        logger.info(f"Collecting search result videos on {page_request}")
        video_info_one_page = extract_video_info_in_search_result_page(page_request)
        search_result_video_info.update(video_info_one_page)
        
    # do second-hand ranking, based on uploading time or review counts
    sorted_bvs = list(search_result_video_info.keys())
    if sort_option == "1":
        sorted_bvs =  rank_video_view_count(search_result_video_info)
    elif sort_option == "2":
        sorted_bvs = rank_video_upload_date(search_result_video_info)
    max_videos = min(len(sorted_bvs), max_videos)
    candidate_video_bvs = sorted_bvs[:max_videos]

    print("\n\n----------------------------------------------------------")
    logger.info("Collecting videos information done!")

    # Filter candidate videos and retrive basic info - av & oid
    print("\n\n----------------------------------------------------------")
    logger.info("Filtering candidate videos and retriving video av & oid ...\n") 
    candidate_video_urls = [search_result_video_info[bv]["video_url"] for bv in candidate_video_bvs]
    # candidate_video_urls = candidate_video_urls[:1] ### DEBUG ONLY!!!!!!
    candidate_video_info = retrive_relevant_videos_info(keyword, candidate_video_urls)
    # print(candidate_video_info)

    # Scrape danmaku and comments of filtered videos
    for i,bv in enumerate(candidate_video_info.keys()):
        print("\n\n----------------------------------------------------------\n\n")
        logger.info(f"Progress: {i+1}/{len(candidate_video_info)}")
        logger.info(f"Working on video https://www.bilibili.com/video/BV{bv}")
        av = candidate_video_info[bv]["av"]
        sex_list, comment_list = extract_info_from_video_comments(av)
        oid = candidate_video_info[bv]["oid"]
        danmaku_list = extract_danmaku(oid)
        candidate_video_info[bv]["sex_list"] = sex_list
        candidate_video_info[bv]["comment_list"] = comment_list
        candidate_video_info[bv]["danmaku_list"] = danmaku_list

    print("\n\n----------------------------------------------------------")
    logger.info("Retriving danmaku & comments done!")

    return search_result_video_info, candidate_video_info
    

if __name__ == "__main__":
    start = time.time()
    query = "arknights"
    search_result_video_info, candidate_video_info = start_scraping(query, max_pages=50, max_videos=1)
    print("\n==== Search Result videos from query word ====\n")
    for bv in search_result_video_info.keys():
        print(f"https://www.bilibili.com/video/BV{bv}:", search_result_video_info[bv])
        print("\n")

    print("\n==== Candidate videos for retriving danmaku & comments ======\n")
    for bv in candidate_video_info.keys():
        print(f"https://www.bilibili.com/video/BV{bv}:", candidate_video_info[bv])
        print("\n")
    elasped = time.time() - start
    print(f"total time: {elasped} seconds")

