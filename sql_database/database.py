from peewee import *
from .config import db_path
from model.model import Bookmarks

db = db_path

class SQLTrailDB():

    def insert_trail(self, id, name, type, difficulty, stars, location, length, ascent, descent, condition_details, url):
        Bookmarks.create(id=id, name=name, trailtype=type, difficulty=difficulty, stars=stars, location=location, length=length, ascent=ascent, descent=descent, condition_details=condition_details, url=url)
        
    def remove_trail(self, id):
        query = Bookmarks.delete().where(Bookmarks.id == id)
        query.execute()