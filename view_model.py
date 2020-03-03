from model.model import Bookmarks

class ViewModel:
    
    def __init__(self, db):
        self.db = db

    def insertTrail(self, trail):
        Bookmarks.save(trail)

    def deleteTrail(self, bookmark_id):
        Bookmarks.delete().where(Bookmarks.id == bookmark_id).execute()