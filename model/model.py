from peewee import *
from sql_database.config import db_path

db = SqliteDatabase(db_path)

# Peewee configuration
class BaseModel(Model):
    class Meta:
        database = db

class Bookmarks(BaseModel):
    id = IntegerField()
    name = CharField()
    trailtype = CharField()
    difficulty = CharField()
    stars = FloatField()
    location = CharField()
    url = CharField()
    length = FloatField()
    ascent = FloatField()
    descent = FloatField()
    longitude = FloatField()
    latitude = FloatField()
    condition_details = CharField()

db.connect()
db.create_tables(Bookmarks)