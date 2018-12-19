import os

# folder of the application
APP_DIR = str(os.path.dirname(os.path.abspath(__file__)))

# Google API KEY
GOOGLE_API_KEY = 'AIzaSyBrpyh7_0Xl2FpfPr1XnBHFcFQJzzlTZec'


# database configs
DB_FILE_NAME = os.path.join(APP_DIR, 'databases/database.ini')
DB_SECTION = 'postgresql'

# database tables and columns
DB_PLACES_TABLE = 'Places'
DB_PLACES_ID_COLUMN = 'PlaceId'
DB_PLACES_COLUMNS = {
    'name':     'Name',
    'website':  'Website',
    'address':  'Address',
    'city':     'City',
    'place_id': 'GooglePin',
    'loc_x':    'CoordinateX',
    'loc_y':    'CoordinateY',
    'phone':    'Phone',
}

DB_WORKING_TIME_TABLE = 'WorkingTime'
DB_WORKING_TIME_COLUMNS = {
    'place_id':  'PlaceId',
    'days':      'Days',
    'open_time': 'OpenTime',
}

# folder to save menus
MENUS_DIR = 'data/menus'
