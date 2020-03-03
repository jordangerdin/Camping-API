from model.model import Bookmarks

class ViewModel:
    
    def __init__(self, db):
        self.db = db

    def insertTrail(self, trail):
        Bookmarks.save(trail)

    def getTrails(self):
        query = Bookmarks.select().dicts()
        return query

    def deleteTrail(self, bookmark_id):
        Bookmarks.delete().where(Bookmarks.id == bookmark_id).execute()