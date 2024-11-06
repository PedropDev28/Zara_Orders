from pymongo import MongoClient
from django.conf import settings

def get_db_handle():
    client = MongoClient(
        host=settings.MONGODB_HOST,
        port=settings.MONGODB_PORT,
        username=settings.MONGODB_USER,
        password=settings.MONGODB_PASSWORD
    )
    db_handle = client[settings.MONGODB_NAME]
    return db_handle, client