import os

import pandas as pd

from collect_places.google_maps import GoogleMapService as gms
from collect_places.parquet import read_parquet
from config import REQUESTS_DIR


class GoogleMapService(gms):
    """
    Class to replace original `GoogleMapService` class
    """

    def __init__(self):
        pass

    def get_places_nearby(self, *args, **kwargs) -> pd.DataFrame:
        """
        Get places nearby
        :return: data from the request
        """
        response_file = ''
        return read_parquet(os.path.join(REQUESTS_DIR, response_file))

    def get_info_about_place(self, *args, **kwargs) -> pd.DataFrame:
        """
        Get detailed information about place
        :return:  data from the request
        """
        response_file = ''
        return read_parquet(os.path.join(REQUESTS_DIR, response_file))

    def get_places(self, *args, **kwargs) -> pd.DataFrame:
        """
        Get places and details info about them nearby
        :return: data from the request
        """
        response_file = 'places.parquet'
        return read_parquet(os.path.join(REQUESTS_DIR, response_file))
