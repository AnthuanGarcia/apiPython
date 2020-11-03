import os
from flask_pymongo import pymongo

DB_USER = os.getenv("DB_USER")
DB_PASSW = os.getenv("DB_PASSW")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
AUTH = os.getenv("AUTH")

client = pymongo.MongoClient(f"mongodb+srv://{DB_USER}:{DB_PASSW}@db-apipython.tubxs.mongodb.net/{DB_NAME}?retryWrites=true&w=majority")
db = client.RetroConsolas