import json
import pandas as pd

from tqdm import tqdm

from app.google_maps.google_map import (
    places_nearby_search, place_details
)


class GoogleMapService(object):

    def __init__(self):
        super(GoogleMapService, self).__init__()

    def get_places_nearby(self, location=None, type_='restaurant', radius=1000, response_file=None):
        """
        Get places nearby
        If response_file is defined google maps request will not be done

        :param location: coordinates of start point
        :type location: tuple
        :param type_: type of places
        :type type_: str
        :param radius: radius of the search circle
        :type radius: int
        :param response_file: name of the file where there is json object of place_details response
        :type response_file: str:
        :return: pandas.DataFrame
        """

        if response_file:
            with open(f'data/responses/{response_file}', 'r') as file:
                obj = json.loads(file.read(), encoding='utf-8')
        else:
            obj = places_nearby_search(
                location=location,
                type_=type_,
                radius=radius,
                page_token=None,
            )

        if obj:
            res = self.split_dict(obj=obj, single=False)
        else:
            return None

        return pd.DataFrame(data=list(zip(*res.values())), columns=res.keys())

    def get_info_about_place(self, place_id, response_file=None):
        """
        Get detailed information about place
        If response_file is defined google maps request will not be done

        :param place_id: google id of the place
        :type place_id: str
        :param response_file: name of the file where there is json object of place_details response
        :type response_file: str
        :return: pandas.DataFrame
        """

        if response_file:
            with open(f'data/responses/{response_file}', 'r') as file:
                obj = json.loads(file.read(), encoding='utf-8')
        else:
            obj = place_details(
                place_id=place_id,
                page_token=None,
            )

        if obj:
            res = self.split_dict(obj=obj, single=True)
        else:
            return None

        return pd.DataFrame(data=list(zip(*res.values())), columns=res.keys())

    def get_places(self, location=None, type_='restaurant', radius=1000, response_file=None):
        """
        Get places and details info about them nearby
        If response_file is defined google maps request will not be done

        :param location: coordinates of start point
        :type location: tuple
        :param type_: type of places
        :type type_: str
        :param radius: radius of the search circle
        :type radius: int
        :param response_file: name of the file where there is json object of place_details response
        :type response_file: str:
        :return: pandas.DataFrame
        """

        detailed_data = dict()
        df = self.get_places_nearby(location=location, type_=type_, radius=radius, response_file=response_file)
        if df is None:
            return None
        for place_id in tqdm(df.place_id, desc='Detailed info', total=df.shape[0]):
            obj = place_details(
                place_id=place_id,
                page_token=None,
            )
            if obj:
                res = self.split_dict(obj=obj, single=True)
            else:
                continue

            for k in res.keys() - detailed_data.keys():
                detailed_data[k] = [None] * len(next(iter(detailed_data.values()), []))
            for k, v in detailed_data.items():
                v.append(res.get(k))

        if not detailed_data:
            return None
        return pd.DataFrame(data=detailed_data)

    def split_dict(self, obj, single=False):
        """
        Parse json object to dictionary

        :param obj: object to split
        :param single: if obj consist of one single element
        :type single: bool
        :return: dictionary with all nested keys
        """

        dict_ = dict()

        if not single:
            size = len(obj)

            for index, item in enumerate(obj):
                dict_ = self.get_values(obj=item, size=size, dict_=dict_, index=index)
        else:
            dict_ = self.get_values(obj=obj, size=1, dict_=dict_, index=0)
        return dict_

    def get_values(self, obj, size, dict_, index, key=None):
        """
        Recursive reading of the nested dictionary

        :param obj: object to read
        :param dict_: resulted dictionary
        :type dict_: dict
        :param size: size of the original object
        :type size: int
        :param key: key of the current object
        :type key: str
        :param index: original index of current object
        :type index: int
        :return: dictionary
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
