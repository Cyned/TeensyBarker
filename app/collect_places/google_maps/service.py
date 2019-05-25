import pandas as pd

from tqdm import tqdm
from typing import Tuple, Optional

from collect_places.google_maps.google_map import places_nearby_search, place_details
from app import collect_logger as logger


class GoogleMapService(object):
    """
    Class to manipulate and preprocess data from the GoogleMaps API
    """

    def __init__(self):
        super(GoogleMapService, self).__init__()

    def get_places_nearby(self, location: Tuple[float, float], type_: str, radius: int) -> Optional[pd.DataFrame]:
        """
        Get places nearby
        :param location: coordinates of start point
        :param type_: type of places
        :param radius: radius of the search circle
        :return: data from the request
        """
        obj = places_nearby_search(location=location, type_=type_, radius=radius, page_token='')
        if not obj:
            return None
        res = self.split_dict(obj=obj, single=False)
        return pd.DataFrame(data=list(zip(*res.values())), columns=res.keys())

    def get_info_about_place(self, place_id: str) -> Optional[pd.DataFrame]:
        """
        Get detailed information about place
        :param place_id: google id of the place
        :return: data from the request
        """
        obj = place_details(place_id=place_id, page_token='')
        if not obj:
            return None
        res = self.split_dict(obj=obj, single=True)
        return pd.DataFrame(data=list(zip(*res.values())), columns=res.keys())

    def get_places(self, location: Tuple[float, float], type_: str, radius: int) -> Optional[pd.DataFrame]:
        """
        Get places and details info about them nearby
        :param location: coordinates of start point
        :param type_: type of places
        :param radius: radius of the search circle
        :return: data from the request
        """
        detailed_data: dict = dict()
        df = self.get_places_nearby(location=location, type_=type_, radius=radius)
        if df is None:
            return None
        logger.debug('Get places. Go to the detailed information...')
        for place_id in tqdm(df.place_id, desc='Detailed info', total=df.shape[0]):
            obj = place_details(place_id=place_id, page_token='')
            if not obj:
                continue
            res = self.split_dict(obj=obj, single=True)
            for k in res.keys() - detailed_data.keys():
                detailed_data[k] = [None] * len(next(iter(detailed_data.values()), []))
            for k, v in detailed_data.items():
                v.append(res.get(k))

        if not detailed_data:
            logger.info('No data')
            return None
        return pd.DataFrame(data=detailed_data)

    def split_dict(self, obj: dict, single: bool = False) -> dict:
        """
        Parse json object to dictionary
        :param obj: object to split
        :param single: if obj consist of one single element
        :return: dictionary with all nested keys
        """
        dict_: dict = dict()
        if not single:
            size = len(obj)
            for index, item in enumerate(obj):
                dict_ = self.get_values(obj=item, size=size, dict_=dict_, index=index)
        else:
            dict_ = self.get_values(obj=obj, size=1, dict_=dict_, index=0)
        return dict_

    def get_values(self, obj: dict, size: int, dict_, index: int, key: str = '') -> dict:
        """
        Recursive reading of the nested dictionary
        :param obj: object to read
        :param dict_: resulted dictionary
        :param size: size of the original object
        :param key: key of the current object
        :param index: original index of current object
        :return:
        """

        if isinstance(obj, dict):
            for mini_key in obj.keys():
                if key:
                    tmp_key = f'{key}_{mini_key}'
                else:
                    tmp_key = mini_key
                dict_ = self.get_values(obj=obj[mini_key], size=size, dict_=dict_, index=index, key=tmp_key)
        else:
            if key not in dict_.keys():
                dict_[key] = [None] * size
            dict_[key][index] = str(obj)

        return dict_
