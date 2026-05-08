"""
MongoDB database initialization
"""
from flask_pymongo import PyMongo

mongo = PyMongo()

def get_db():
    """Return the MongoDB database instance"""
    return mongo.db
