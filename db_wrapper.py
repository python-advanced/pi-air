from pymongo import MongoClient
from datetime import datetime, timezone


class DBWrapper:
    def __init__(self):
        self.client = MongoClient('mongodb+srv://allen:YToAqiPX2VQ20a0v@cluster0.wf5gy.mongodb.net/air?retryWrites=true&w=majority')
        self.db = self.client.air

    def insert_data(self, voc_ccs, voc_tgs, pm25, pm10):
        at = datetime.now(timezone.utc)
        d = {
            'VOC-CCS': voc_ccs, 
            'VOC-TGS': voc_tgs,
            'PM25': pm25, 
            'PM10': pm10,
            'at': at,
        }
        self.db.air.insert_one(d)
