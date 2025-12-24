import os
import pandas as pd
from datetime import datetime, date
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

MONGO_URI = os.getenv("mongodb+srv://<niroops05>:<niroopS05R>@cluster0.kxe6ry3.mongodb.net/?appName=Cluster0")

REQUIRED_COLUMNS = ["Date", "Region", "Product", "Units Sold", "Revenue"]

def get_collection():
    if not MONGO_URI:
        return None
    try:
        client = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=5000
        )
        db = client["sales_db"]
        return db["sales"]
    except ServerSelectionTimeoutError:
        return None

def normalize_date(value):
    if isinstance(value, date) and not isinstance(value, datetime):
        return datetime.combine(value, datetime.min.time())
    return value

def fetch_all_sales():
    collection = get_collection()
    if collection is None:
        return pd.DataFrame(columns=REQUIRED_COLUMNS)

    try:
        data = list(collection.find({}, {"_id": 0}))
        if not data:
            return pd.DataFrame(columns=REQUIRED_COLUMNS)
        return pd.DataFrame(data)
    except ServerSelectionTimeoutError:
        return pd.DataFrame(columns=REQUIRED_COLUMNS)

def insert_sale(sale):
    collection = get_collection()
    if collection is None:
        raise RuntimeError("Database not reachable")

    sale["Date"] = normalize_date(sale["Date"])
    collection.insert_one(sale)
