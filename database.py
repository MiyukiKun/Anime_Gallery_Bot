from pymongo.collection import Collection
from config import client, database_name


class ConfigDB:
    def __init__(self):
        self.col = Collection(client[database_name], 'ConfigDB')
        
    def find(self, data):
        return self.col.find_one(data)

    def add(self, data):
        self.col.insert_one(data)

    def modify(self, search_dict, new_dict):
        try:
            self.col.find_one_and_update(search_dict, {'$set': new_dict})
        except Exception as e:
            print(f"Exception in ConfigDB -> modify\n\n{e}")

class UsersDB:
    def __init__(self):
        self.files_col = Collection(client[database_name], 'UsersDB')
        
    def find(self, data):
        return self.files_col.find_one(data)
    
    def full(self):
        return list(self.files_col.find())

    def add(self, data):
        try:
            self.files_col.insert_one(data)
        except:
            pass

    def remove(self, data):
        self.files_col.delete_one(data)