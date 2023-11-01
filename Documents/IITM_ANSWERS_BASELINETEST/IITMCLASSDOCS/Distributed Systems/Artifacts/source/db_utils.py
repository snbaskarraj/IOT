from pymongo import MongoClient
from bson.objectid import ObjectId
import math
import random
import time
import datetime

def connect_mongo(host, port):
    mongo_client = None
    try:
        mongo_client = MongoClient(f'mongodb://{host}:{port}')
        print("Connection successful")
        return mongo_client

    except Exception as e:
        print("An exception occurred ::", e)
        return mongo_client


def create_database(host, port, db_name):
    db_conn = connect_mongo(host, port)
    db_conn.drop_database(db_name)
    db = db_conn[db_name]
    return db
