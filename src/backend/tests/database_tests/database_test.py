import unittest
import src.backend.database.mongoDB as db


class DataBaseTests(unittest.TestCase):

    def setUp(self):
        """ prepare testing data """
        self.test_data = (
            {"1rK4y1p7Cs": {"view_count": 2882785.7821422517, "upload_date": {"date": 1612828800000},
                "author": {"\u6e0a\u6e0a\u7684\u5947\u5999\u5192\u9669":
                           "https://www.bilibil.com/space.bilibili.com/440454918?from=search"},
                "video_url": "https://www.bilibili.com/video/BV1rK4y1p7Cs?from=search"}}
        )

    def tearDown(self):
        data_base = db.get_db()
        record = data_base.get_collection("candidate_videos")
        record.delete_many({})

    def test_upload(self):
        """ test upload data to candidate videos collection """
        data_base = db.get_db()
        records = data_base.get_collection("candidate_videos")
        db.insert_document("candidate_videos", self.test_data)
        self.assertEqual(records.count_documents({}), 1)

    def test_delete(self):
        """ test delete document in a certain collection """
        data_base = db.get_db()
        record = data_base.get_collection("candidate_videos")
        db.insert_document("candidate_videos", self.test_data)
        db.clean("candidate_videos", {})
        self.assertEqual(record.count_documents({}), 0)
