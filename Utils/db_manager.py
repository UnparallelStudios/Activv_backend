import os

from datetime import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


class DbManager :
    def __init__(self) :
        self.uri = os.environ.get("URI")
        print(f"URI is : {self.uri}")
        self.client = MongoClient(self.uri, server_api=ServerApi('1'))
        print("Connection established with mongodb")
        
        self.db = None
        self.collection = None


    def load_db(self, sem, branch) :
        # finds the appropriate database from the current year and the given semester
        ch1, ch2 = f"{sem}-{datetime.today().year}", f"{sem}-{datetime.today().year-1}"
        print(f"ch1, ch2: {ch1}, {ch2}")
        db_names = self.client.list_database_names()
        print(f"db_names: {db_names}")
        db = ch1 if ch1 in db_names else ch2 if ch2 in db_names else None
        print(f"db: {db}")
        if db :
            collection_names = self.client[db].list_collection_names()
            print(f"collection_names: {collection_names}")
            print(f"branch: {branch} collection_names: {collection_names} {branch in collection_names}")
            if branch in collection_names :
                print("IN BRANCH")
                self.db = self.client[db]
                self.collection = self.db[branch]
                return 1
            else :
                print("NOT IN BRANCH")                
        print("Did not enter condition")
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