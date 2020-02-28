class ViewModel:
    
    def __init__(self, db):
        self.db = db

    def insertTrail(self, id, name, type, difficulty, stars, location, length, ascent, descent, condition_details, url):
        self.db.insert_trail(id, name, type, difficulty, stars, location, length, ascent, descent, condition_details, url)

    def deleteTrail(self, id):
        self.db.remove_trail(id)