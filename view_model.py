class ViewModel:
    
    def __init__(self, db):
        self.db = db

    def insertTrail(self, id, name, trailtype, difficulty, stars, location, url, length, ascent, descent, longitude, latitude, condition_details):
        self.db.insert_trail(id, name, trailtype, difficulty, stars, location, url, length, ascent, descent, longitude, latitude, condition_details)

    def deleteTrail(self, id):
        self.db.remove_trail(id)