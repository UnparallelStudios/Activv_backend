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
        self.db = self.client[f"{sem}-{datetime.today().year}"]
        self.collection = self.db[branch]

        
    def total_no_classes(self, sem, branch) :
        """Total no of classes per subject"""
        # Load the user's database onto memory
        self.load_db(sem, branch)
        return self.collection.find({}, {"_id": 0})[0]