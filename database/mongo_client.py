import os
from pymongo import MongoClient
import pandas as pd
from datetime import datetime, date
MONGO_URI =  "mongodb+srv://niroops05:niroopS05R@cluster0.kxe6ry3.mongodb.net/"

client = MongoClient(MONGO_URI)
db = client["sales_db"]
collection = db["sales"]

def normalize_date(value):
    """
    Convert date → datetime for MongoDB compatibility
    """
    if isinstance(value, date) and not isinstance(value, datetime):
        return datetime.combine(value, datetime.min.time())
    return value

def insert_sale(sale_dict):
    # Normalize Date field
    if "Date" in sale_dict:
        sale_dict["Date"] = normalize_date(sale_dict["Date"])

    collection.insert_one(sale_dict)

def fetch_all_sales():
    data = list(collection.find({}, {"_id": 0}))
    return pd.DataFrame(data)
