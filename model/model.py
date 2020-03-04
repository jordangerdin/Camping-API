from peewee import *
from sql_database.config import db_path

db = SqliteDatabase(db_path)

# Peewee configuration
class BaseModel(Model):
    class Meta:
        database = db

class Bookmarks(BaseModel):
    trail_id = IntegerField()
    name = CharField()
    trail_type = CharField(null=True)
    difficulty = CharField(null=True)
    stars = FloatField(null=True)
    location = CharField(null=True)
    url = CharField()
    length = FloatField(null=True)
    ascent = FloatField(null=True)
    descent = FloatField(null=True)
    longitude = FloatField(null=True)
    latitude = FloatField(null=True)
    condition_details = CharField(null=True)

db.connect()
db.create_tables([Bookmarks])