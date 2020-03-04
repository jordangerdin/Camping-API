import os
#import book_wishlist
#from book_wishlist import app
from main import app
import unittest
import tempfile
from model.model import Bookmarks

from unittest import TestCase
from peewee import *

import sql_database.config

sql_database.config.db_path = 'test_trails.sqlite'
database = SqliteDatabase(sql_database.config.db_path)

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def remake_tables(self):
        database.drop_tables([Bookmarks])
        database.create_tables([Bookmarks])
    
    def add_test_data(self):
        self.trail1 = Bookmarks.create(trail_id = '11l23j1', name = 'A Beautiful Trail', trail_type='Hiking', difficulty='Green', stars='5', location='Somewhere lovely', url='https://www.trailinfo.com/beauty', length=5, ascent=5, descent=5, longitude=44, latitude=-102, condition_details='It\'s Really Pretty')
        self.trail2 = Bookmarks.create(trail_id = '1231o1oj', name = 'A Less Beautiful Trail', trail_type='Hiking', difficulty='GreenBlue', stars='3', location='Somewhere okay, I guess', url='https://www.trailinfo.com/could_be_worse', length=10, ascent=4, descent=1, longitude=3, latitude=-50, condition_details='It sure exists')
        self.trail3 = Bookmarks.create(trail_id = 'l24j23lj', name = 'A Hidious Trail', trail_type='Hiking', difficulty='Red', stars='-5', location='Somewhere awful', url='https://www.trailinfo.com/dear_god_why', length=55, ascent=-4, descent=13, longitude=123, latitude=50, condition_details='It\'s even worse then you feared')
