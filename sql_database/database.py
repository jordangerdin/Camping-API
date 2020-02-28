from peewee import *
from .config import db_path
from model.model import Bookmarks

db = db_path

class SQLTrailDB():

    def insert_trail(self, id, name, type, difficulty, stars, location, url, length, ascent, descent, longitude, latitude, condition_details):
        Bookmarks.create(id=id, name=name, trailtype=type, difficulty=difficulty, stars=stars, location=location, url=url, length=length, ascent=ascent, descent=descent, longitude=longitude, latitude=latitude, condition_details=condition_details)
        
    def remove_trail(self, id):
        query = Bookmarks.delete().where(Bookmarks.id == id)
        query.execute()