import argparse

from collect_places.google_maps import GoogleMapService
from databases import BDPlaces
from app import collect_logger as logger


def get_args():
    parser = argparse.ArgumentParser(description='Update Places Postgres database')
    parser.add_argument('--loc_x', type=float, default=50.445990)
    parser.add_argument('--loc_y', type=float, default=30.440773)
    parser.add_argument('--type', type=str, default='restaurant')
    parser.add_argument('--radius', type=int, default=10000)
    parser.add_argument('--response_file', type=str, default='')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    google_map = GoogleMapService()

    data = google_map.get_places(
        location=(args.loc_x, args.loc_y), type_=args.type, radius=args.radius,
    )
    if data is not None:
        data = data.applymap(lambda x: x[0] if x else x)

        with BDPlaces() as db:
            db.test()
            db.add(data=data)
            for item in db.get_place(columns=['name', 'website']):
                print(item)
            print(db.get_working_time(place_ids=(101,)))
    else:
        logger.info('There is no data got from GoogleMaps API')
