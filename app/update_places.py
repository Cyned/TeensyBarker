import argparse

from collect_places.google_maps import GoogleMapService
from databases import DBPlaces
from timeit import timeit_context
from app import collect_logger as logger


def get_args():
    parser = argparse.ArgumentParser(description='Update Places Postgres database')
    parser.add_argument('--loc_x', type=float, default=50.445000)
    parser.add_argument('--loc_y', type=float, default=30.440005)
    parser.add_argument('--type', type=str, default='restaurant')
    parser.add_argument('--radius', type=int, default=10000)
    parser.add_argument('--response_file', type=str, default='')
    return parser.parse_args()


if __name__ == '__main__':
    with timeit_context('Total time execution'):
        args = get_args()
        google_map = GoogleMapService()

        data = google_map.get_places(
            location=(args.loc_x, args.loc_y), type_=args.type, radius=args.radius,
        )
        if data is None:
            logger.info('There is no data got from GoogleMaps API')
        else:
            data = data.applymap(lambda x: x[0] if x else x)
            data['name'] = data.name.str.lower()
            with DBPlaces() as db:
                db.add_places(data=data)
