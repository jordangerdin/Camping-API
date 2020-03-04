from unittest import TestCase
from model.model import Bookmarks
from peewee import *

test_db = SqliteDatabase(':memory:')

class TestHikingDB(TestCase):
    
    def setUp(self):
        test_db.bind([Bookmarks], bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables([Bookmarks])

    def tearDown(self):
        Bookmarks.drop_table()
        test_db.close()

    def test_add_new_trail(self):
        self.trail = Bookmarks.create(trail_id=1, name='High Falls and Two Step Falls', trail_type='Hike', difficulty='blue', stars=4.8, location='Finland, Minnesota', url='https://www.hikingproject.com/trail/7035597/high-falls-and-two-step-falls', length=3.6, ascent=528, descent=-528, longitude=-91.1158, latitude=47.209, condition_details='All Clear')

        trail_count = Bookmarks.select().count()
        self.assertEqual(1, trail_count)

    def test_remove_trail(self):
        self.trail = Bookmarks.create(trail_id=2, name='High Falls and Two Step Falls', trail_type='Hike', difficulty='blue', stars=4.8, location='Finland, Minnesota', url='https://www.hikingproject.com/trail/7035597/high-falls-and-two-step-falls', length=3.6, ascent=528, descent=-528, longitude=-91.1158, latitude=47.209, condition_details='All Clear')

        query = Bookmarks.delete().where(Bookmarks.trail_id == 2)
        rows_changed = query.execute()

        self.assertEqual(1, rows_changed)


if __name__=='__main__':
    import unittest
    main()