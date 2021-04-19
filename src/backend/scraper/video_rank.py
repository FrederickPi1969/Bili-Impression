import datetime

def rank_video_upload_date(all_video_info):
    """
    :param all_video_info: dictionary bv to video info (max size 1000)
    :return: sorted keys of dictionary (or sorted bv) based on video upload date,
            or unsorted keys if error occurred.
    """
    try:
        return sorted(all_video_info, 
                    key=lambda bv: all_video_info[bv]["upload_date"],
                    reverse=True)
    except:
        print('Key "upload_date" is missing in argument video info dictionary')
        return list(all_video_info.keys())



def rank_video_view_count(all_video_info):
    """
    :param all_video_info: dictionary bv to video info (max size 1000)
    :return: sorted keys of dictionary (or sorted bv) based on video view count
            or unsorted keys if error occurred.
    """
    try:
        return sorted(all_video_info, 
                    key=lambda bv : all_video_info[bv]["view_count"], 
                    reverse=True)
    except:
        print('Key "view_count" is missing in argument video info dictionary.')
        return list(all_video_info.keys())


if __name__ == "__main__": 
    all_video_info = {'1Ax411a72W': {'view_count': 6290338.837654055, 'upload_date': datetime.datetime(2017, 6, 3, 0, 0), 'author': {'=咬人猫=': 'https://www.bilibil.com/space.bilibili.com/116683?from=search'}, 'video_url': 'https://www.bilibili.com/video/BV1Ax411a72W?from=search'}, '11E411e7M8': {'view_count': 4688279.679485343, 'upload_date': datetime.datetime(2019, 11, 12, 0, 0), 'author': {}, 'video_url': 'https://www.bilibili.com/video/BV11E411e7M8?from=search'}, '174411V7mS': {'view_count': 3810708.1092897747, 'upload_date': datetime.datetime(2019, 6, 15, 0, 0), 'author': {'视角姬': 'https://www.bilibil.com/space.bilibili.com/52250?from=search'}, 'video_url': 'https://www.bilibili.com/video/BV174411V7mS?from=search'}, '1S4411K7ey': {'view_count': 3130355.8343144073, 'upload_date': datetime.datetime(2019, 6, 8, 0, 0), 'author': {'视角姬': 'https://www.bilibil.com/space.bilibili.com/52250?from=search'}, 'video_url': 'https://www.bilibili.com/video/BV1S4411K7ey?from=search'}, '17p411R7jh': {'view_count': 2932444.7286607893, 'upload_date': datetime.datetime(2018, 5, 25, 0, 0), 'author': {'=咬人猫=': 'https://www.bilibil.com/space.bilibili.com/116683?from=search'}, 'video_url': 'https://www.bilibili.com/video/BV17p411R7jh?from=search'}, '1fZ4y1n7fT': {'view_count': 2576156.0159290964, 'upload_date': datetime.datetime(2020, 6, 1, 0, 0), 'author': {'碧蓝航线': 'https://www.bilibil.com/space.bilibili.com/233114659?from=search'}, 'video_url': 'https://www.bilibili.com/video/BV1fZ4y1n7fT?from=search'}, '1ox411S7pU': {'view_count': 2568954.2810430177, 'upload_date': datetime.datetime(2017, 4, 14, 0, 0), 'author': {'哔哩哔哩游戏中心': 'https://www.bilibil.com/space.bilibili.com/1328260?from=search'}, 'video_url': 'https://www.bilibili.com/video/BV1ox411S7pU?from=search'}, '1ez411v7H7': {'view_count': 2460926.7213406884, 'upload_date': datetime.datetime(2020, 7, 17, 0, 0), 'author': {'烟季': 'https://www.bilibil.com/space.bilibili.com/15377173?from=search'}, 'video_url': 'https://www.bilibili.com/video/BV1ez411v7H7?from=search'}, '1P4411p7e2': {'view_count': 2261335.9309610347, 'upload_date': datetime.datetime(2019, 5, 31, 0, 0), 'author': {'=咬人猫=': 'https://www.bilibil.com/space.bilibili.com/116683?from=search'}, 'video_url': 'https://www.bilibili.com/video/BV1P4411p7e2?from=search'}, '1MW411b73u': {'view_count': 2251791.738640504, 'upload_date': datetime.datetime(2018, 1, 1, 0, 0), 'author': {'碧蓝航线': 'https://www.bilibil.com/space.bilibili.com/233114659?from=search'}, 'video_url': 'https://www.bilibili.com/video/BV1MW411b73u?from=search'}, '1YW411Q7fU': {'view_count': 2163307.199794268, 'upload_date': datetime.datetime(2018, 8, 22, 0, 0), 'author': {'鱼干悠暧Official': 'https://www.bilibil.com/space.bilibili.com/22042016?from=search'}, 'video_url': 'https://www.bilibili.com/video/BV1YW411Q7fU?from=search'}, '1bK411n7BG': {'view_count': 2054832.1388233644, 'upload_date': datetime.datetime(2020, 6, 14, 0, 0), 'author': {'我是怪异君': 'https://www.bilibil.com/space.bilibili.com/4408538?from=search'}, 'video_url': 'https://www.bilibili.com/video/BV1bK411n7BG?from=search'}, '1Mx411p7J8': {'view_count': 2011988.61639816, 'upload_date': datetime.datetime(2017, 8, 5, 0, 0), 'author': {'LexBurner': 'https://www.bilibil.com/space.bilibili.com/777536?from=search'}, 'video_url': 'https://www.bilibili.com/video/BV1Mx411p7J8?from=search'}, '1z4411K7sx': {'view_count': 1979938.914671389, 'upload_date': datetime.datetime(2019, 6, 7, 0, 0), 'author': {'=咬人猫=': 'https://www.bilibil.com/space.bilibili.com/116683?from=search'}, 'video_url': 'https://www.bilibili.com/video/BV1z4411K7sx?from=search'}, '1uJ41137Gx': {'view_count': 1888461.8840447527, 'upload_date': datetime.datetime(2019, 9, 19, 0, 0), 'author': {'番剧资 讯姬': 'https://www.bilibil.com/space.bilibili.com/408002864?from=search'}, 'video_url': 'https://www.bilibili.com/video/BV1uJ41137Gx?from=search'}, '1Ha411F7AV': {'view_count': 1809672.0075576631, 'upload_date': datetime.datetime(2020, 11, 30, 0, 0), 'author': {'江之岛绫小路': 'https://www.bilibil.com/space.bilibili.com/39112946?from=search'}, 'video_url': 'https://www.bilibili.com/video/BV1Ha411F7AV?from=search'}, '1Jt411Y76E': {'view_count': 1616172.0537406225, 'upload_date': datetime.datetime(2018, 12, 21, 0, 0), 'author': {'视角姬': 'https://www.bilibil.com/space.bilibili.com/52250?from=search'}, 'video_url': 'https://www.bilibili.com/video/BV1Jt411Y76E?from=search'}, '187411N7pq': {'view_count': 1592400.8873356495, 'upload_date': datetime.datetime(2020, 2, 29, 0, 0), 'author': {'BML制作指挥部': 'https://www.bilibil.com/space.bilibili.com/403748305?from=search'}, 'video_url': 'https://www.bilibili.com/video/BV187411N7pq?from=search'}, '1bx411Y7mm': {'view_count': 1557666.2078659167, 'upload_date': datetime.datetime(2017, 5, 26, 0, 0), 'author': {'敖厂长': 'https://www.bilibil.com/space.bilibili.com/122879?from=search'}, 'video_url': 'https://www.bilibili.com/video/BV1bx411Y7mm?from=search'}, '19r4y1F7dB': {'view_count': 1548656.0395065488, 'upload_date': datetime.datetime(2020, 11, 23, 0, 0), 'author': {'一色OneColors': 'https://www.bilibil.com/space.bilibili.com/17497051?from=search'}, 'video_url': 'https://www.bilibili.com/video/BV19r4y1F7dB?from=search'}}
    # ranked_bvs = rank_video_view_count(all_video_info)
    # for bv in ranked_bvs:
    #     print(all_video_info[bv])

    ranked_bvs = rank_video_upload_date(all_video_info)
    for bv in ranked_bvs:
        print(all_video_info[bv])
