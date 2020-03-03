from peewee import *
from .config import db_path
from model.model import Bookmarks

db = db_path

class SQLTrailDB():

    def insert_trail(self, trail):
        Bookmarks.save(trail)
        
    def remove_trail(self, id):
        query = Bookmarks.delete().where(Bookmarks.id == id)
        query.execute()