import sys
import argparse

import pandas as pd

from google_maps import GoogleMapService
from databases import BDPlaces


def get_args():
    parser = argparse.ArgumentParser(description='Update Places Postgres database')
    parser.add_argument('--loc_x', type=float, default=50.447230)
    parser.add_argument('--loc_y', type=float, default=30.522673)
    parser.add_argument('--type', type=str, default='restaurant')
    parser.add_argument('--radius', type=int, default=10000)
    parser.add_argument('--response_file', type=str, default='')
    return parser.parse_args()


if __name__ == '__main__':

    # args = get_args()
    # google_map = GoogleMapService()
    #
    # df = google_map.get_places(location=(args.loc_x, args.loc_y),
    #                            type_=args.type,
    #                            radius=args.radius,
    #                            response_file=args.response_file,
    #                            )
    # if df is not None:
    #     df.to_csv('data/khreschatyk_new.csv', index=False)
    # else:
    #     sys.exit('Error')

    df = pd.read_csv('data/khreschatyk_new.csv').fillna('')

    with BDPlaces() as db:
        db.test()
        db.add(data=df)
        for item in db.get_place(columns=['name', 'website']):
            print(item)
        print(db.get_working_time(place_ids=93))
    pass
