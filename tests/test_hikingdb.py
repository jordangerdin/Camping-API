from unittest import TestCase
from model.model import Bookmarks
from peewee import *

class TestHikingDB(TestCase):
    
    def setUp(self):
        self.db = SqliteDatabase(':memory:')
        self.db.drop_tables([Bookmarks])
        self.db.create_tables([Bookmarks])

    def test_add_new_trail(self):
        trail = Bookmarks.create(trail_id=1, name='High Falls and Two Step Falls', trail_type='Hike', difficulty='blue', stars=4.8, location='Finland, Minnesota', url='https://www.hikingproject.com/trail/7035597/high-falls-and-two-step-falls', length=3.6, ascent=528, descent=-528, longitude=-91.1158, latitude=47.209, condition_details='All Clear')

        trail_count = Bookmarks.select().count()
        self.assertEqual(1, trail_count)

    def test_remove_trail(self):
        trail = Bookmarks.create(trail_id=2, name='High Falls and Two Step Falls', trail_type='Hike', difficulty='blue', stars=4.8, location='Finland, Minnesota', url='https://www.hikingproject.com/trail/7035597/high-falls-and-two-step-falls', length=3.6, ascent=528, descent=-528, longitude=-91.1158, latitude=47.209, condition_details='All Clear')

        query = Bookmarks.delete().where(Bookmarks.trail_id == 2)
        rows_changed = query.execute()

        self.assertEqual(1, rows_changed)


if __name__=='__main__':
    import unittest
    main()