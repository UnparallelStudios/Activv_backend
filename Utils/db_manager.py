import os

from datetime import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


class DbManager :
    def __init__(self, sem="S4", branch="AD") :
        self.uri = os.environ.get("URI")
        self.client = MongoClient(self.uri, server_api=ServerApi('1'))
        print("Connection established with mongodb")

        # finds the appropriate database from the current year and the given semester
        self.db = self.client[f"{sem}-{datetime.today().year}"]
        self.collection = self.db[branch]

        
    def total_no_classes(self) :
        return self.collection.find({}, {"_id": 0})



if __name__ == "__main__" :
    from dotenv import load_dotenv
    
    load_dotenv()

    db_manager = DbManager()
    total = db_manager.total_no_classes()
    for i in total :
        print(i)