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
    trail_type = CharField()
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

    def __str__(self):
        return f'ID {self.id}, Name: {self.name}'

db.connect()
db.create_tables([Bookmarks])