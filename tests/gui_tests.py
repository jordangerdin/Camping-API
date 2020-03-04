from main import app
import unittest
from model.model import Bookmarks
from unittest import TestCase
from peewee import *
import api_connection
from routes import *

# we got the idea to put the database into memory from the Peewee documentation.
test_db = SqliteDatabase(':memory:')

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

        # This binds the model to the database
        test_db.bind([Bookmarks], bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables([Bookmarks])

        trailsDB = test_db
        trailsViewModel = view_model.ViewModel(trailsDB)

    def tearDown(self):
        trail_dictionary = {}
        Bookmarks.drop_table()
        test_db.close()

    def add_test_data(self):
        self.trail1 = Bookmarks.create(trail_id = '11l23j1', name = 'A Beautiful Trail', trail_type='Hiking', difficulty='Green', stars='5', location='Somewhere lovely', url='https://www.trailinfo.com/beauty', length=5, ascent=5, descent=5, longitude=44, latitude=-102, condition_details='It\'s Really Pretty')
        self.trail2 = Bookmarks.create(trail_id = '1231o1oj', name = 'A Less Beautiful Trail', trail_type='Hiking', difficulty='GreenBlue', stars='3', location='Somewhere okay, I guess', url='https://www.trailinfo.com/could_be_worse', length=10, ascent=4, descent=1, longitude=3, latitude=-50, condition_details='It sure exists')
        self.trail3 = Bookmarks.create(trail_id = 'l24j23lj', name = 'A Hidious Trail', trail_type='Hiking', difficulty='Red', stars='-5', location='Somewhere awful', url='https://www.trailinfo.com/dear_god_why', length=55, ascent=-4, descent=13, longitude=123, latitude=50, condition_details='It\'s even worse then you feared')

    def test_empty_database(self):
        page = self.app.get('/view_saved')
        assert b'No Trails.' in page.data

        page = self.app.get('/find_trails')
        assert b'No Trails.' in page.data

    def test_view_saved_trails(self):
        self.add_test_data()

        page = self.app.get('/view_saved')
        assert b'A Beautiful Trail' in page.data
        assert b'A Less Beautiful Trail' in page.data
        assert b'A Hidious Trail' in page.data

    def test_no_data_in_table_that_wasnt_saved(self):
        self.add_test_data()

        page = self.app.get('/view_saved')
        assert b'This is not part of the added data' not in page.data

    def test_delete_data(self):
        self.add_test_data()

        trailsViewModel.deleteTrail('11l23j1')
        page = self.app.get('/view_saved')
        assert b'A Beautiful Trail' not in page.data
        assert b'A Less Beautiful Trail' in page.data 

        
    """ Commented out becaue I cannot find how to get past the loc_form.validate_on_submit()
    @patch('api_connection.get_lat_lon')    
    @patch('api_connection.get_hiking_data')
    def test_search_trail(self, mock_get_hiking_data, mock_get_lat_lon):
        mock_trail_responce = { "trails": [ { "id": 7000130, "name": "Bear Peak Out and Back", "type": "Hike", "summary": "A must-do hike for Boulder locals and visitors alike!", "difficulty": "blueBlack", "stars": 4.6, "starVotes": 112, "location": "Boulder, Colorado", "url": "https://www.hikingproject.com/trail/7000130/bear-peak-out-and-back", "imgSqSmall": "https://cdn-files.apstatic.com/hike/7005382_sqsmall_1554312030.jpg", "imgSmall": "https://cdn-files.apstatic.com/hike/7005382_small_1554312030.jpg", "imgSmallMed": "https://cdn-files.apstatic.com/hike/7005382_smallMed_1554312030.jpg", "imgMedium": "https://cdn-files.apstatic.com/hike/7005382_medium_1554312030.jpg", "length": 5.7, "ascent": 2541, "descent": -2540, "high": 8342, "low": 6103, "longitude": -105.2755, "latitude": 39.9787, "conditionStatus": "Minor Issues", "conditionDetails": "Snowy, Icy", "conditionDate": "2020-01-12 10:26:32" }, { "id": 7011192, "name": "Boulder Skyline Traverse", "type": "Hike", "summary": "The classic long mountain route in Boulder.", "difficulty": "black", "stars": 4.7, "starVotes": 75, "location": "Superior, Colorado", "url": "https://www.hikingproject.com/trail/7011192/boulder-skyline-traverse", "imgSqSmall": "https://cdn-files.apstatic.com/hike/7048859_sqsmall_1555540136.jpg", "imgSmall": "https://cdn-files.apstatic.com/hike/7048859_small_1555540136.jpg", "imgSmallMed": "https://cdn-files.apstatic.com/hike/7048859_smallMed_1555540136.jpg", "imgMedium": "https://cdn-files.apstatic.com/hike/7048859_medium_1555540136.jpg", "length": 16.3, "ascent": 5409, "descent": -5492, "high": 8492, "low": 5417, "longitude": -105.2582, "latitude": 39.9388, "conditionStatus": "All Clear", "conditionDetails": "Some Mud", "conditionDate": "2020-01-25 16:47:26" }, { "id": 7004226, "name": "Sunshine Lion's Lair Loop", "type": "Hike", "summary": "Great Mount Sanitas views are the reward for this gentler loop in Sunshine Canyon.", "difficulty": "blue", "stars": 4.5, "starVotes": 107, "location": "Boulder, Colorado", "url": "https://www.hikingproject.com/trail/7004226/sunshine-lions-lair-loop", "imgSqSmall": "https://cdn-files.apstatic.com/hike/7039883_sqsmall_1555092747.jpg", "imgSmall": "https://cdn-files.apstatic.com/hike/7039883_small_1555092747.jpg", "imgSmallMed": "https://cdn-files.apstatic.com/hike/7039883_smallMed_1555092747.jpg", "imgMedium": "https://cdn-files.apstatic.com/hike/7039883_medium_1555092747.jpg", "length": 5.3, "ascent": 1261, "descent": -1282, "high": 6800, "low": 5530, "longitude": -105.2979, "latitude": 40.02, "conditionStatus": "Minor Issues", "conditionDetails": "Snowy, Some Mud - lower and middle parts of Sunshine Canyon were muddy and slick, but overall traction wasn't necessary. completely dry on Lion's Lair and descent", "conditionDate": "2020-01-05 20:47:44" }, { "id": 7011191, "name": "Green Mountain via Ranger/Saddle Rock Loop", "type": "Hike", "summary": "A loop with a variety of terrain, a lot of climbing, and great views of Boulder.", "difficulty": "blueBlack", "stars": 4.5, "starVotes": 78, "location": "Boulder, Colorado", "url": "https://www.hikingproject.com/trail/7011191/green-mountain-via-rangersaddle-rock-loop", "imgSqSmall": "https://cdn-files.apstatic.com/hike/7003740_sqsmall_1554235436.jpg", "imgSmall": "https://cdn-files.apstatic.com/hike/7003740_small_1554235436.jpg", "imgSmallMed": "https://cdn-files.apstatic.com/hike/7003740_smallMed_1554235436.jpg", "imgMedium": "https://cdn-files.apstatic.com/hike/7003740_medium_1554235436.jpg", "length": 4.9, "ascent": 2305, "descent": -2277, "high": 8099, "low": 5806, "longitude": -105.2928, "latitude": 39.9975, "conditionStatus": "Minor Issues", "conditionDetails": "Some Mud, Icy - Shoe microspikes recommended for sections. Amounts to about half of the trail.", "conditionDate": "2020-01-25 16:28:25" }, { "id": 7004682, "name": "Royal Arch Out and Back", "type": "Hike", "summary": "A classic Boulder hike to a natural arch with great views.", "difficulty": "blueBlack", "stars": 4.4, "starVotes": 148, "location": "Boulder, Colorado", "url": "https://www.hikingproject.com/trail/7004682/royal-arch-out-and-back", "imgSqSmall": "https://cdn-files.apstatic.com/hike/7002679_sqsmall_1554226731.jpg", "imgSmall": "https://cdn-files.apstatic.com/hike/7002679_small_1554226731.jpg", "imgSmallMed": "https://cdn-files.apstatic.com/hike/7002679_smallMed_1554226731.jpg", "imgMedium": "https://cdn-files.apstatic.com/hike/7002679_medium_1554226731.jpg", "length": 3.3, "ascent": 1311, "descent": -1312, "high": 6917, "low": 5691, "longitude": -105.283, "latitude": 39.9997, "conditionStatus": "Minor Issues", "conditionDetails": "Icy - Some wet/muddy areas and scattered ice but minor", "conditionDate": "2020-02-02 15:56:29" }, { "id": 7002439, "name": "Walker Ranch", "type": "Hike", "summary": "An awesome and challenging hike near Boulder with great scenery.", "difficulty": "blueBlack", "stars": 4.5, "starVotes": 121, "location": "Coal Creek, Colorado", "url": "https://www.hikingproject.com/trail/7002439/walker-ranch", "imgSqSmall": "https://cdn-files.apstatic.com/hike/7039625_sqsmall_1555092312.jpg", "imgSmall": "https://cdn-files.apstatic.com/hike/7039625_small_1555092312.jpg", "imgSmallMed": "https://cdn-files.apstatic.com/hike/7039625_smallMed_1555092312.jpg", "imgMedium": "https://cdn-files.apstatic.com/hike/7039625_medium_1555092312.jpg", "length": 7.6, "ascent": 1594, "descent": -1585, "high": 7335, "low": 6439, "longitude": -105.3378, "latitude": 39.9511, "conditionStatus": "Minor Issues", "conditionDetails": "Dry, Muddy, Snowy, Icy", "conditionDate": "2019-11-24 16:15:01" }, { "id": 7000000, "name": "Mount Sanitas Loop", "type": "Hike", "summary": "Very popular and scenic loop right from the edge of town.", "difficulty": "blueBlack", "stars": 4.2, "starVotes": 106, "location": "Boulder, Colorado", "url": "https://www.hikingproject.com/trail/7000000/mount-sanitas-loop", "imgSqSmall": "https://cdn-files.apstatic.com/hike/7039883_sqsmall_1555092747.jpg", "imgSmall": "https://cdn-files.apstatic.com/hike/7039883_small_1555092747.jpg", "imgSmallMed": "https://cdn-files.apstatic.com/hike/7039883_smallMed_1555092747.jpg", "imgMedium": "https://cdn-files.apstatic.com/hike/7039883_medium_1555092747.jpg", "length": 3.2, "ascent": 1281, "descent": -1280, "high": 6780, "low": 5521, "longitude": -105.2977, "latitude": 40.0202, "conditionStatus": "All Clear", "conditionDetails": "Dry", "conditionDate": "2020-01-26 11:10:58" }, { "id": 7001019, "name": "Betasso Preserve", "type": "Hike", "summary": "This hike is easily accessible from Boulder and offers amazing singletrack with beautiful views.", "difficulty": "blue", "stars": 4.1, "starVotes": 61, "location": "Boulder, Colorado", "url": "https://www.hikingproject.com/trail/7001019/betasso-preserve", "imgSqSmall": "https://cdn-files.apstatic.com/hike/7029200_sqsmall_1554920151.jpg", "imgSmall": "https://cdn-files.apstatic.com/hike/7029200_small_1554920151.jpg", "imgSmallMed": "https://cdn-files.apstatic.com/hike/7029200_smallMed_1554920151.jpg", "imgMedium": "https://cdn-files.apstatic.com/hike/7029200_medium_1554920151.jpg", "length": 6.7, "ascent": 776, "descent": -778, "high": 6575, "low": 6178, "longitude": -105.3446, "latitude": 40.0164, "conditionStatus": "Minor Issues", "conditionDetails": "Mostly Dry - Icey in spots", "conditionDate": "2020-01-25 12:03:18" }, { "id": 7017569, "name": "Marshall Mesa to Spring Brook Loop", "type": "Hike", "summary": "Some of the best trails that Boulder has to offer with a variety of options that never get old.", "difficulty": "blue", "stars": 4.3, "starVotes": 26, "location": "Superior, Colorado", "url": "https://www.hikingproject.com/trail/7017569/marshall-mesa-to-spring-brook-loop", "imgSqSmall": "https://cdn-files.apstatic.com/hike/7002458_sqsmall_1554226116.jpg", "imgSmall": "https://cdn-files.apstatic.com/hike/7002458_small_1554226116.jpg", "imgSmallMed": "https://cdn-files.apstatic.com/hike/7002458_smallMed_1554226116.jpg", "imgMedium": "https://cdn-files.apstatic.com/hike/7002458_medium_1554226116.jpg", "length": 11.1, "ascent": 893, "descent": -893, "high": 6236, "low": 5567, "longitude": -105.2313, "latitude": 39.9527, "conditionStatus": "All Clear", "conditionDetails": "Some Mud", "conditionDate": "2020-01-25 16:47:13" }, { "id": 7005887, "name": "Sugarloaf Mountain", "type": "Hike", "summary": "The best bang-for-your-buck view trail in Boulder County.", "difficulty": "greenBlue", "stars": 4.4, "starVotes": 19, "location": "Boulder, Colorado", "url": "https://www.hikingproject.com/trail/7005887/sugarloaf-mountain", "imgSqSmall": "https://cdn-files.apstatic.com/hike/7031490_sqsmall_1554931128.jpg", "imgSmall": "https://cdn-files.apstatic.com/hike/7031490_small_1554931128.jpg", "imgSmallMed": "https://cdn-files.apstatic.com/hike/7031490_smallMed_1554931128.jpg", "imgMedium": "https://cdn-files.apstatic.com/hike/7031490_medium_1554931128.jpg", "length": 1.4, "ascent": 432, "descent": -432, "high": 8892, "low": 8460, "longitude": -105.4251, "latitude": 40.0255, "conditionStatus": "Unknown", "conditionDetails": 'null', "conditionDate": "1970-01-01 00:00:00" } ], "success": 1 }
        mock_get_hiking_data.return_value = mock_trail_responce

        mock_lat_lon_responce = { "documentation": "https://opencagedata.com/api", "licenses": [ { "name": "see attribution guide", "url": "https://opencagedata.com/credits" } ], "rate": { "limit": 2500, "remaining": 2467, "reset": 1583366400 }, "results": [ { "annotations": { "DMS": { "lat": "50° 58' 49.44000'' N", "lng": "11° 19' 34.68000'' E" }, "MGRS": "32UPB6329550221", "Maidenhead": "JO50px95dh", "Mercator": { "x": 1260837.949, "y": 6584609.52 }, "OSM": { "note_url": "https://www.openstreetmap.org/note/new#map=16/50.98040/11.32630&layers=N", "url": "https://www.openstreetmap.org/?mlat=50.98040&mlon=11.32630#map=16/50.98040/11.32630" }, "UN_M49": { "regions": { "DE": "276", "EUROPE": "150", "WESTERN_EUROPE": "155", "WORLD": "001" }, "statistical_groupings": [ "MEDC" ] }, "callingcode": 49, "currency": { "alternate_symbols": [], "decimal_mark": ",", "html_entity": "&#x20AC;", "iso_code": "EUR", "iso_numeric": "978", "name": "Euro", "smallest_denomination": 1, "subunit": "Cent", "subunit_to_unit": 100, "symbol": "€", "symbol_first": 1, "thousands_separator": "." }, "flag": "🇩🇪", "geohash": "u30418xw3gm7sft30f5c", "qibla": 132.4, "roadinfo": { "drive_on": "right", "speed_in": "km/h" }, "sun": { "rise": { "apparent": 1583301180, "astronomical": 1583294640, "civil": 1583299200, "nautical": 1583296920 }, "set": { "apparent": 1583341200, "astronomical": 1583347800, "civil": 1583343180, "nautical": 1583345520 } }, "timezone": { "name": "Europe/Berlin", "now_in_dst": 0, "offset_sec": 3600, "offset_string": "+0100", "short_name": "CET" }, "what3words": { "words": "divisions.crass.slicing" } }, "components": { "ISO_3166-1_alpha-2": "DE", "ISO_3166-1_alpha-3": "DEU", "_category": "postcode", "_type": "postcode", "continent": "Europe", "country": "Germany", "country_code": "de", "political_union": "European Union", "postcode": "99423" }, "confidence": 7, "formatted": "99423, Germany", "geometry": { "lat": 50.9804, "lng": 11.3263 } } ], "status": { "code": 200, "message": "OK" }, "stay_informed": { "blog": "https://blog.opencagedata.com", "twitter": "https://twitter.com/opencagedata" }, "thanks": "For using an OpenCage API", "timestamp": { "created_http": "Wed, 04 Mar 2020 13:58:14 GMT", "created_unix": 1583330294 }, "total_results": 1 }
        mock_get_lat_lon = mock_lat_lon_responce['results'][0]['geometry']

        page = self.app.post('/find_trails', data=dict(city='Test City', state='TS'), follow_redirects=True)
        assert b'Bear Peak Out and Back' in page.data
        
    Tests I would write if I could:
        
        give lat_lon api bad city/state
        give hiking api bad lat/lon

        get weather
        get weather no selection

        I don't know how to write tests for the map even more then I don't know how to write tests for the forms but
            get map
            get map no selection 
        
        save trail using the save button
        delete trail using the delete button

        try saving no selection
        try deleting no selection
        """

if __name__ == '__main__':
    unittest.main()