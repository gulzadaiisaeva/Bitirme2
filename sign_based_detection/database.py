from pymongo import MongoClient
from os import walk
import hashlib

client = MongoClient('localhost:27017')
db = client.maldect
virus_collection = db['virushash']
files = []


def getallFiles(folder):
    for (dirpath, dirnames, filenames) in walk(folder):
        files.extend(filenames)
        break
    print(files)

def insert_database(folder):
    for i in files:
        with open(folder + '/' + i, 'rb') as file_to_check:
            data = file_to_check.read()
            md5_returned = hashlib.md5(data).hexdigest()
        print(md5_returned)

        isExist = virus_collection.find_one({'md5': md5_returned})

        if (isExist != None):
            print_status("Status:", "   This Object is already exist in MongoDB!! md5 : ", str(isExist['md5']))
        else:
            jsonFile = {
                "md5": md5_returned
            }
            virus_collection.insert(jsonFile)
            print("Status:", "   Data successfully stored in MongoDB!! md5 : ",str(jsonFile['md5']))

getallFiles("../exevirus")
insert_database("../exevirus")


