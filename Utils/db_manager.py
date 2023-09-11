import os

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


class DbManager :
    def __init__(self) :
        self.uri = os.environ.get("URI")
        self.client = MongoClient(self.uri, server_api=ServerApi('1'))
        print("Connection established with mongodb")
        
        self.db = None
        self.collection = None


    def load_db(self, pass_out_year, branch) :
        # finds the appropriate database from the current year and the given semester
        db_names = self.client.list_database_names()
        if pass_out_year in db_names :
            self.db = self.client[str(pass_out_year)]
            if branch in self.db.list_collection_names() :
                self.collection = self.db[branch]
                return 1
        
        self.db = None
        return 0

        
    def total_no_classes(self, pass_out_year, branch) :
        """Total no of classes per subject"""
        # Load the user's database onto memory
        status = self.load_db(pass_out_year, branch)
        if status :
            return self.collection.find({}, {"_id": 0})[0]
        else :
            return None
        
    
    def update_classes(self, classes, pass_out_year, branch) :
        status = self.load_db(pass_out_year, branch)
        if status :
            class_total = self.collection.find_one()
            print(f"Initial database looked like: {class_total}")
            id = class_total["_id"]
            for period in classes :
                class_total[period] += int(classes[period])
            
            # Update the db
            self.collection.update_one({'_id':id}, {"$set": class_total}, upsert=False)
            print(f"Updated database looks like: {class_total}")
            
            return 1
        else :
            return 0