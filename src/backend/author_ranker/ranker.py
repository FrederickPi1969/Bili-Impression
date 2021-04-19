# import src.backend.scraper.scraper as scraper
import numpy as np
import pickle as pkl

def view_count_enhanced_func(x):
    """
    :x: index of the video in one author's video list (0,1,2,3,4,5...)
    This is the function we will use for weighted cumulative view count.
    See demo for intuitive understanding.
    """
    return 1 + 0.01 * (x ** 1.5) + (x < 5) * (x > 0) * 0.15 * x ** 1.35 \
           + (x >= 5) * ((-0.01 * (5 ** 1.5)) + 0.15 * 5 **1.35)


def construct_author2vc(search_result_video_info):
    """
    Collect the historical view count of different authors.
    :param search_result_video_info: search result video info dict collected by scraper/scraper
    :return: Recorded statistics as a dict with format {author1:[vc1, vc2...], author2:[vc1...]}
    """
    author2vc = {} # vc as view count
    for bv in list(search_result_video_info.keys()):
        author_info = search_result_video_info[bv]["author"]
        author_name = list(author_info.keys())[0]
        view_count = search_result_video_info[bv]["view_count"]
        if author_name not in author2vc:
            author2vc[author_name] = [view_count]
        else:
            # Top ranked (recommended) videos should have larger weight
            author2vc[author_name].insert(0, view_count)
    return author2vc


def calculate_author2wcc(author2vc):
    """
    Calculate authors' view count enhanced weighted cumulative view count.
    :author2vc: author2view_count constructed by construct_author2vc.
    :return: dict {author1: wcc1, ...}
    """
    author2wcc = {}  # wcc as weighted cumulative counts
    func = np.vectorize(view_count_enhanced_func)
    for author, view_counts in author2vc.items():
        weights = func(np.arange(len(view_counts)))
        wcc = np.sum(np.array(view_counts) * weights)
        author2wcc[author] = wcc
    return author2wcc

def calc_author_total_views_naive(author2vc):
    """
    Calculate each author's total view counts by naively summing up all his videos' view counts.
    :author2vc: author2view_count constructed by construct_author2vc.
    :return: dict {author1: tv1, ...}
    """
    author2tv = {}  # total views
    for author, view_counts in author2vc.items():
        vc = np.sum(view_counts)
        author2tv[author] = vc
    return author2vc

def find_top_k_authors(search_result_video_info, k=10, corrected=True):
    """
    Interface for running the topk author module.
    Calculate and returns the most popular authors based on corrected cumulative view count.
    :param search_result_video_info: FIRST return value of backend/scraper/scraper.py/start_scraping.
        usually we collect 1000 for one query.
    :param corrected: whether to the weight enhanced cumulative view count for ranking. If not naive
        algorithm will be used (raw total view count).
    :return: a list of authors, desceding order (No.1, No.2,...).
    """
    author2vc = construct_author2vc(search_result_video_info)
    author2value = calculate_author2wcc(author2vc) if corrected else calc_author_total_views_naive(author2vc)
    top_authors = sorted(author2value, key=lambda author: author2value[author], reverse=True) # Descending order
    end_index = min(len(top_authors), k)
    return top_authors[:end_index]


if __name__ == "__main__":
    # topic = "游戏"
    # search_result_video_info, _ = \
    #     scraper.start_scraping(topic, max_pages=50, max_videos=1)
    # with open(f"./{topic}.pkl", "wb+") as file:
    #     pkl.dump(search_result_video_info, file)
    # print(find_top_k_authors(search_result_video_info, 25))
    pass
