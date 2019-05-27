import argparse

from tqdm import tqdm

from collect_menus import Place
from databases import DBPlaces
from config import DB_PLACES_ID_COLUMN
from app import parser_logger as logger


def update_menus():
    """ Update menus data """
    parser = argparse.ArgumentParser(description='Update Places Postgres database')
    return parser.parse_args()


if __name__ == "__main__":
    # Process websites one by one
    with DBPlaces() as db:
        results = db.get_places(columns=(DB_PLACES_ID_COLUMN, 'website'))
    for place_id, website in tqdm(results, total=len(results), desc='Search menus'):
        if website:
            logger.info(f'Start analyzing {place_id}: {website}')
            restaurant = Place(website=website, place_id=str(place_id))
            restaurant.collect_menu()
        else:
            logger.info(f'No website: {place_id}')
