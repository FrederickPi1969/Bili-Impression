import src.backend.database.mongoDB as db



data = {"1rK4y1p7Cs": {"view_count": 2882785.7821422517, "upload_date": {"date": 1612828800000},
                "author": {"\u6e0a\u6e0a\u7684\u5947\u5999\u5192\u9669":
                           "https://www.bilibil.com/space.bilibili.com/440454918?from=search"},
                "video_url": "https://www.bilibili.com/video/BV1rK4y1p7Cs?from=search"}}
records = db.insert_document("candidate_videos", data)

# records = db.clean("candidate_videos", data)