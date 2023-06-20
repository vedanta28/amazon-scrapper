from bottomTable import getdata
from pymongo import MongoClient
import json
import sys
import os
import time

#load environment variables
with open('.env') as f:
    for line in f:
        key, value = line.strip().split('=')
        os.environ[key] = value

def dbConnector():
    conn_string=os.environ["CON_STR"]
    conn_string=conn_string.replace('<password>',os.environ["PASSWORD"])
    client = None
    while client is None:
        try:
            client = MongoClient(conn_string)
        except:
            time.sleep(1)
            print("Error connecting to database.")

    # Access a specific database
    database = client[os.environ["DB_NAME"]]

    # Access a specific collection within the database
    collection = database["products"]
    return collection



def main():
    url = sys.argv[1]
    print(json.dumps(getdata(url), indent=4))
    collection=dbConnector()
    document=json.loads(json.dumps(getdata(url)))
    collection.insert_one(document)

if __name__ == "__main__":
    main()