from view import *
from sql_database.database import SQLTrailDB
from view.view import View
from view_model import ViewModel

def main():
    
    trailsDB = SQLTrailDB
    
    trailsViewModel = ViewModel(trailsDB)

    # Should be replaced by frontend HTML
    trailsView = View(trailsViewModel)

    trailsView.add_new_trail()

if __name__ == '__main__':
    main()