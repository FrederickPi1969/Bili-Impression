import sys
sys.path.append("./")
import unittest
from src.backend.popularity_kde import kde_estimator as ke
from datetime import datetime,timedelta
from bs4 import BeautifulSoup
import requests
import numpy as np
import pickle as pkl

NOW = datetime.now()
class TestKdeEstimator(unittest.TestCase):
    def test_date_grid_very_old(self):
        """
        1. Test that date grid constructor can construct date grids correctly for a very old video.
        """
        upload_date = datetime(2010, 10, 8)
        current_year, current_month = NOW.year, NOW.month
        grids = ke.construct_month_grids(upload_date)
        self.assertTrue(grids[0] == "2010-10")
        self.assertTrue(grids[-1] ==f"{current_year}-{current_month}")
        self.assertTrue(len(grids) > 12 * 10)

    def test_date_grid_today(self):
        """
        2. Test that date grid constructor can construct date grids correctly for a fairly new video (today).
        """
        current_year, current_month, current_day = NOW.year, NOW.month, NOW.day
        upload_date = datetime(current_year, current_month, current_day)
        grids = ke.construct_month_grids(upload_date)
        self.assertTrue(grids[0] ==f"{current_year}-{current_month}")
        self.assertTrue(len(grids) == 1)

    def test_total_days_calculations(self):
        """
        3. Test help function calc_total_days can correctly output total days.
        """
        self.assertTrue(ke.calc_total_days(datetime(2018, 10, 21), datetime(2018, 10, 29)) == 8)
        self.assertTrue(ke.calc_total_days(datetime(2004, 2, 21), datetime(2004, 3, 1)) == 9) # Feb has 29 days in 2004!
        self.assertTrue(ke.calc_total_days(datetime(2016, 1, 1), datetime(2017, 1, 1)) == 366)

    def test_min_max_scale_date_hptc_anchors(self):
        """
        4. Test hptc min-max scaler can scale anchor points (06/26/2009, 04/01/2021, NOW) correctly.
        """
        self.assertTrue(ke.min_max_scale_date_hptc(NOW) > 1)
        self.assertTrue(ke.min_max_scale_date_hptc(datetime(2009, 6, 26)) == 0)
        self.assertTrue(ke.min_max_scale_date_hptc(datetime(2021, 4, 1)) == 1)

    def test_min_max_scale_date_hptc_random(self):
        """
        5. Test hptc min-max scaler can scale random selected dates correctly.
        """
        one = ke.calc_total_days(datetime(2009, 6, 26), datetime(2009, 6, 26))
        # first random date
        date1 = datetime(2012, 6, 18)
        mapped_date1 = ke.calc_total_days(datetime(2009, 6, 26), date1) / one
        self.assertTrue(ke.min_max_scale_date_hptc(date1), mapped_date1 / one)

        # second random date
        date2 = datetime(2029, 1, 1)
        mapped_date2 = ke.calc_total_days(datetime(2009, 6, 26), date2) / one
        self.assertTrue(ke.min_max_scale_date_hptc(date2), mapped_date2 / one)

        # thrid random date
        date3 = datetime(2000, 2, 10)
        mapped_date3 = ke.calc_total_days(datetime(2009, 6, 26), date3) / one
        self.assertTrue(ke.min_max_scale_date_hptc(date3), mapped_date3 / one)

    def test_RI_is_shifted_correctly_old_video(self):
        """
        6. Test that RI would scale correctly (i.e. y values mapped correctly) when range does not match with hptc
            for a old video.
        """
        unshifted_start_val, unshifted_end_val = ke.remeberance_index(0, 95), ke.remeberance_index(1, 95) # 0, 1
        upload_date = datetime(2016, 10, 8)
        mapped_uplod_date = ke.min_max_scale_date_hptc(upload_date) # 0 mapped to upload_date
        mapped_today = ke.min_max_scale_date_hptc(NOW)  # 1 mapped to today
        shifted_start_val, shifted_end_val = ke.remeberance_index(mapped_uplod_date, 95, mapped_uplod_date, mapped_today),\
                                             ke.remeberance_index(mapped_today, 95, mapped_uplod_date, mapped_today)
        self.assertEqual(unshifted_start_val, shifted_start_val) # RI_unshifted(0, 95) == RI_shifted(upload, 95)
        self.assertEqual(unshifted_end_val, shifted_end_val)

    def test_RI_is_shifted_correctly_new_video(self):
        """
        7. Test that RI would scale correctly (i.e. y values mapped correctly) when range does not match with hptc
            for a new video that is published today.
        """
        unshifted_start_val, unshifted_end_val = ke.remeberance_index(0, 95), ke.remeberance_index(1, 95) # 0, 1
        upload_date = datetime(NOW.year, NOW.month, NOW.day)
        mapped_uplod_date = ke.min_max_scale_date_hptc(upload_date) # 0 mapped to upload_date
        mapped_today = ke.min_max_scale_date_hptc(NOW)  # 1 mapped to today
        shifted_start_val, shifted_end_val = ke.remeberance_index(mapped_uplod_date, 95, mapped_uplod_date, mapped_today),\
                                             ke.remeberance_index(mapped_today, 95, mapped_uplod_date, mapped_today)
        self.assertEqual(unshifted_start_val, shifted_start_val) # RI_unshifted(0, 95) == RI_shifted(upload, 95)
        self.assertEqual(unshifted_end_val, shifted_end_val)

    def test_calc_percentile(self):
        """
        8. Test percentile video is calculated correctly.
        """
        with open("./美食.pkl", "rb+") as file:
            search_result_video_info = pkl.load(file)
            bv2vpd = ke.calc_corrected_vpd(search_result_video_info)
            bv2percentile = ke.calc_vpd_percentile(bv2vpd)
            for i in range(100):
                bv1, bv2 = np.random.choice(list(bv2vpd.keys()), 2, replace=False)
                if bv2vpd[bv1] >=  bv2vpd[bv2]:
                    self.assertTrue(bv2percentile[bv1] >= bv2percentile[bv2])
                else:
                    self.assertTrue(bv2percentile[bv1] < bv2percentile[bv2])

    def test_kde_outputs_correct_cumulative_view_count(self):
        """
        9. Test that monthly view count estimated by kde sums up to correct total view count
        """
        with open("./美食.pkl", "rb+") as file:
            search_result_video_info = pkl.load(file)
            month2vc = ke.construct_month2vc_all_search_result_videos(search_result_video_info)
            for bv in month2vc:
                truth = search_result_video_info[bv]["view_count"]
                estimated_sum = np.sum(list(month2vc[bv].values()))
                self.assertTrue((truth - estimated_sum) / truth < 0.01) # < 1% error rate

    def test_kde_outputs_correct_decay_tendency(self):
        """
        10. Test that prediction of monthly view count follows the gamma-decay tendency for a quickly-chaging area
            such as 美食.
        """
        with open("./美食.pkl", "rb+") as file:
            search_result_video_info = pkl.load(file)
            month2vc = ke.construct_month2vc_all_search_result_videos(search_result_video_info)
            decay_count = 0
            rise_count = 0
            for bv in month2vc:
                estimated_vcs =  list(month2vc[bv].values())
                if len(estimated_vcs) <= 2: continue
                for i in range(1, len(estimated_vcs) - 1):
                    if estimated_vcs[i] >= estimated_vcs[i + 1]: decay_count += 1
                    else: rise_count += 1
            self.assertTrue(rise_count < 0.1 * decay_count)

if __name__ == "__main__":
    unittest.main()


