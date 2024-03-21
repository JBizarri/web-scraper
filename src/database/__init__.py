import os

from .database import Database

DATABASE_PATH = os.getenv("DATABASE_PATH")
database = Database(DATABASE_PATH)
