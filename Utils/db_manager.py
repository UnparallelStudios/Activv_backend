import os

from datetime import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


class DbManager :
    def __init__(self) :
        self.uri = os.environ.get("URI")
        self.client = MongoClient(self.uri, server_api=ServerApi('1'))
        print("Connection established with mongodb")
        
        self.db = None
        self.collection = None


    def load_db(self, sem, branch) :
        # finds the appropriate database from the current year and the given semester
        ch1, ch2 = f"{sem}-{datetime.today().year}", f"{sem}-{datetime.today().year-1}"
        db_names = self.client.list_database_names()
        db = ch1 if ch1 in db_names else ch2 if ch2 in db_names else None
        if db :
            if branch in self.client[db].list_collection_names() :
                self.db = self.client[db]
                self.collection = self.db[branch]
                
                return 1
        return 0

        
    def total_no_classes(self) :
        """Total no of classes per subject"""
        if self.collection is not None :
            return self.collection.find({}, {"_id": 0})[0]
        else :
            return None
        
    def logout(self) :
        self.db = None
        self.collection = None