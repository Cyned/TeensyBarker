import os

# path to the application
APP_DIR: str = str(os.path.dirname(os.path.abspath(__file__)))
# path to project
PROJECT_DIR: str = APP_DIR[:APP_DIR.rfind('/')]

# Google API KEY
GOOGLE_API_KEY: str = 'AIzaSyBrpyh7_0Xl2FpfPr1XnBHFcFQJzzlTZec'


# database configs
DB_FILE_NAME: str = os.path.join(APP_DIR, 'databases/database.ini')
DB_SECTION: str = 'postgresql'

# database tables and columns
DB_PLACES_TABLE: str = 'Places'
DB_PLACES_ID_COLUMN: str = 'PlaceId'
DB_PLACES_COLUMNS: dict = {
    'name':     'Name',
    'website':  'Website',
    'address':  'Address',
    'city':     'City',
    'place_id': 'GooglePin',
    'loc_x':    'CoordinateX',
    'loc_y':    'CoordinateY',
    'phone':    'Phone',
}

DB_WORKING_TIME_TABLE: str = 'WorkingTime'
DB_WORKING_TIME_COLUMNS: dict = {
    'place_id':  'PlaceId',
    'days':      'Days',
    'open_time': 'OpenTime',
}

# folder to data
MENUS_DIR: str = os.path.join(PROJECT_DIR, 'data/menus/')
REQUESTS_DIR: str = os.path.join(PROJECT_DIR, 'data/requests/')

# use substitute of the GoogleMaps Services
SUBSTITUTE: bool = False
