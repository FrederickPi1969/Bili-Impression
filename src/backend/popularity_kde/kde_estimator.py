import numpy as np
from scipy.stats import percentileofscore
from scipy.integrate import quad
import datetime
import pickle as pkl

NOW = datetime.datetime.now()
def calc_total_days(start_date, end_date):
    """
    Given start data and end date, calculate total days elapsed.
    :param start_date: datetime object, starting
    :param end_date: datetime object, ending
    """
    return np.floor((end_date - start_date).total_seconds() / (24 * 60 * 60))

def vpd_correction_function(total_days):
    """
    VPD correction factor based on total days a video has existed.
    1 day will be 0.35, 365 days will be 0.999.
    """
    return 1 / (1  + np.exp(-1 * (total_days - 31) / 50))

def calc_corrected_vpd(search_result_video_info):
    """
    Calculated the corrected view count per day as described in the demo.a
    :param search_results_video_info: (1000) videos collected in the search result vidoes
    :return: dict of {bv_i: vpd_i}
    """
    bv2vpd = {}
    for bv in search_result_video_info.keys():
        view_count = search_result_video_info[bv]["view_count"]
        upload_date = search_result_video_info[bv]["upload_date"]
        total_days = calc_total_days(upload_date, NOW)
        total_days = min(365 * 5, total_days) # cap up to 5 years for fairness
        total_days = max(1, total_days) # cap down to 1 days for numerical robustness
        vpd = vpd_correction_function(total_days) * view_count / total_days
        bv2vpd[bv] = vpd
    return bv2vpd

def calc_vpd_percentile(bv2vpd):
    """
    Calculated corrected percentile of search result videos
    :param bv2vpd: dict returned by calc_corrected_vpd
    :return: dict {bv_i : percentie_i}
    """
    bv2percentile = {}
    all_vpds = np.array([v for v in bv2vpd.values()])
    for bv in bv2vpd.keys():
        percentile = percentileofscore(all_vpds, bv2vpd[bv])
        bv2percentile[bv] = percentile
    return bv2percentile

def remeberance_index(x, vpd_percentile, mapped_min=0, mapped_max=1):
    """
    :param x: mapped time since publication. Without mapping, x range
        will be from 0 to 1, inclusively. 0 will be the first day of publication,
        1 will be the day running this alogrithm. After mapping, mapped_min
        will be original 0, and mapped_max will be original 1. (value are same)
    :param vpd_percentile: as with scale of 100. e.g. 49% input 49.
    :param mapped_min: min value after min-max scaling.
    :param mapped_max: max value after min-max scaling.
    """
    vpd_percentile = max(0.001, vpd_percentile)
    scaling_inv = lambda x : (x - mapped_min) / (mapped_max - mapped_min)
    return (10 / (vpd_percentile / 10)) ** (-12 * scaling_inv(x))


def historical_popularity_tendency(x):
    """
    Notice this is what we refer to as "hptc", c as curve in this module.
    :param x: the time point at which observation is made.
        range from 0 to infinity, where 0 stands for 06/26/2009 - bili establish date
        and 1 stands for 01/04/2021, where this curve was fitted.
        Notice in this function 0 and 1 has a invariant significance!
    """
    return 1 / (1 + np.exp(-8 * (x - 0.75)))


def min_max_scale_date_hptc(date_to_scale):
    """
    min-max scale a given state to fit into the historical_populairty_tendency curve.
    Notice 0 is 06/26asd/2009, 1 is 04/01/2021.
    :param date_to_scale: the date to be scaled.
    :return: mapped scale
    """
    one = datetime.datetime(2021, 4, 1) - datetime.datetime(2009, 6, 26)
    current_scale = date_to_scale - datetime.datetime(2009, 6, 26)
    return current_scale / one


def construct_lvpv_curve(bv, search_result_video_info, bv2percentile):
    """
    Consturct the Long-term Video Popularity Variation Curve (lvpv).
    :param bv: bv number of a video
    :param search search_result_video_info: info of search result videos
    :param bv2percentile: result returned by calc_vpd_percentile
    :return: lvpv ( the kernel to be used in our KDE )
    """
    percentile = bv2percentile[bv]
    upload_date = search_result_video_info[bv]["upload_date"]
    min_max_scale_date_hptc(upload_date)
    upload_date_htpc = min_max_scale_date_hptc(upload_date)
    today_htpc = min_max_scale_date_hptc(NOW)
    def lvpv(x):
        # x follows the scale of hptc!
        # x ranges from update_date_htpc to today_htpc
        return 100 * historical_popularity_tendency(x) * remeberance_index(x, percentile, upload_date_htpc, today_htpc)
    return lvpv

def calc_period_total_view(start, end, lvpv):
    """
    Calculate area under the curve for a certain period.
    :param start: start date (datetime) of the period
    :param end: end date (datetime) of the period
    :param lvpv: the lvpv function specific to a video.
    """
    start_htpc = min_max_scale_date_hptc(start)
    end_htpc = min_max_scale_date_hptc(end)
    val, err = quad(lvpv, start_htpc, end_htpc)
    return max(1e-5, val) # for numeric robustness

def construct_month_grids(upload_date):
    """
    Given the upload date (datetime obj) of a video, construct grided dates as a list,
    with the granularity of month.
    :return: e.g. if upload_date = 02/05/2021, and now=04/08/2021,
        return ['2021-2', '2021-3', '2021-4']
    """
    month_grid = []
    date_iter = upload_date
    while date_iter < NOW:
        if date_iter.day != 1:
            date_iter = datetime.datetime(date_iter.year, date_iter.month, 1)
        month_grid.append(f"{date_iter.year}-{date_iter.month}")
        next_month = date_iter.month + 1
        if next_month == 13:
            date_iter = datetime.datetime(date_iter.year + 1, 1, 1)
        else:
            date_iter = datetime.datetime(date_iter.year, next_month, 1)
        if date_iter > NOW: break
    return month_grid


def construct_month2vc_single_video(bv, search_result_video_info, bv2percentile):
    """
    For a single video, run the KDE algorithm to get its estimated monthly view count.
    :param bv: bv number of the video
    :param search_result_video_info: FIRST return value of backend/scraper/scraper.py/start_scraping.
        usually we collect 1000 for one query.
    :param bv2percentile: return result of calc_vpd_percentile.
    :return: dict, key as return value of construct_month_grid, value as view count for that month.
    """
    upload_date = search_result_video_info[bv]["upload_date"]
    month2vc = {}
    date_grids = construct_month_grids(upload_date)
    lvpv = construct_lvpv_curve(bv, search_result_video_info, bv2percentile)
    total_area =  calc_period_total_view(upload_date, NOW, lvpv)
    total_view_count = search_result_video_info[bv]["view_count"]
    for i, grid_point in enumerate(date_grids):
        year, month  = grid_point.split("-")
        start_date = max(datetime.datetime(int(year), int(month), 1), upload_date)
        if i == len(date_grids) - 1:
            end_date = NOW
        else:
            next_grid_year, next_grid_month = date_grids[i + 1].split("-")
            end_date = datetime.datetime(int(next_grid_year), int(next_grid_month), 1)
        area_this_month = calc_period_total_view(start_date, end_date, lvpv)
        vc_this_month = (area_this_month / total_area) * total_view_count
        month2vc[grid_point] =  vc_this_month
    return month2vc

def construct_month2vc_all_search_result_videos(search_result_video_info):
    """
    Interface for calculating the monthly view count for every single video in the
    search result videos for a given keyword.
    :param search_result_video_info: FIRST return value of backend/scraper/scraper.py/start_scraping.
        usually we collect 1000 for one query.
    :return: A huge dict, key as each videos' bv, value as return value of construct_month2vc_snigle_video.
    """
    bv2vpd = calc_corrected_vpd(search_result_video_info)
    bv2percentile = calc_vpd_percentile(bv2vpd)
    bv2monthly_vc = {}
    for bv in search_result_video_info.keys():
        monthly_vc = construct_month2vc_single_video(bv, search_result_video_info, bv2percentile)
        bv2monthly_vc[bv] = monthly_vc
    return bv2monthly_vc



if __name__ == "__main__":
    with open("./美食.pkl", "rb+") as file:
        search_result_video_info = pkl.load(file)
        month2vc = construct_month2vc_all_search_result_videos(search_result_video_info)
        print(month2vc)
        # bv = "1gp4y1q7S2"
        # bv2vpd = calc_corrected_vpd(search_result_video_info)
        # bv2percentile = calc_vpd_percentile(bv2vpd)
        # lvpv = construct_lvpv_curve(bv, search_result_video_info, bv2percentile)
        # start = search_result_video_info[bv]["upload_date"]
        # end = NOW
        # print(calc_period_total_view(start, end, lvpv))
