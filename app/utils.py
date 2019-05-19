import re
import os
import json

import pandas as pd
import numpy as np

from bs4 import BeautifulSoup
from typing import Tuple, Sequence

from parquet import read_parquet
from config import DB_PLACES_COLUMNS, DB_WORKING_TIME_COLUMNS, REQUESTS_DIR
from working_time import WorkingTime


def transform_df_to_places(data: pd.DataFrame, columns_dict: dict) -> pd.DataFrame:
    """
    Transform DataFrame to needful view for the Places table
    :param data: pandas.DataFrame with GoogleMaps API information
    :param columns_dict: dictionary where values are the columns in current database
    :return: data frame for Places table
    """
    columns = {
        columns_dict['name']     : 'name',
        columns_dict['website']  : 'website',
        columns_dict['place_id'] : 'reference',
        columns_dict['loc_x']    : 'geometry_location_lng',
        columns_dict['loc_y']    : 'geometry_location_lat',
        columns_dict['phone']    : 'international_phone_number',
    }
    df = data[list(columns.values())].rename(columns=dict(zip(columns.values(), columns.keys())))
    if 'adr_address' in data.columns:
        address, city = get_address(data['adr_address'])
        df[columns_dict['address']] = address
        df[columns_dict['city']]    = city
    else:
        df[columns_dict['address']] = []
        df[columns_dict['city']]    = []
    df[columns_dict['phone']] = df[columns_dict['phone']].apply(lambda x: x.replace(' ', '').replace('+', ''))
    return df


def transform_df_to_working_time(data: pd.DataFrame, place_ids: Tuple[Tuple[str, str]], columns_dict: dict) -> pd.DataFrame:
    """
    Transform DataFrame to needful view for the WorkingTime table
    :param data: pandas.DataFrame with GoogleMaps API information
    :param place_ids: ((reference, place_id(in Places table), ...)
    :param columns_dict: dictionary where values are the columns in current database
    :return: dictionary for WorkingTime table
    """
    dict_ = dict(place_ids)
    new_data = data[['reference', 'opening_hours_weekday_text']]
    new_data['place_id'] = new_data['reference'].apply(dict_.get)

    results = dict()
    wt = WorkingTime()
    wt.parse(
        ids=new_data['place_id'],
        times=[get_value(tmp, first=False) for tmp in new_data['opening_hours_weekday_text']],
    )
    if wt.ids:
        results[columns_dict['place_id']]  = wt.ids
        results[columns_dict['days']]      = list(map(int, wt.days))
        results[columns_dict['open_time']] = wt.time
    else:
        return None
    return list(zip(*results.values()))


def delete_existed(data: pd.DataFrame, columns: Tuple[str], results: Tuple[str]) -> pd.DataFrame:
    """
    Delete from current data records that columns have results values
    :param data: data from GoogleMaps API request
    :param columns: columns to compare
    :param results: values to delete in data
    :return: new data frame
    """

    if not columns or not results:
        raise ValueError('Empty attributes')
    results = tuple(zip(*results))
    if len(columns) != len(results):
        raise ValueError('Columns and results attributes have to be one shape.')

    if len(columns) == 1:
        return data.loc[~data[columns[0]].apply(lambda x: get_value(x) in results[0])]
    return data.loc[~np.logical_and(
        *[data[columns[index]].apply(lambda x: get_value(x) in results[index]) for index in range(len(results))]
    )]


def get_address(series: pd.Series) -> Tuple[Sequence, Sequence]:
    """
    Parse html to get address and city of each item of serie.
    :param series: pandas.Series object; HTML with address information
    :return: two numpy.array
    """
    addresses = np.array([None] * len(series))
    cities = np.array([None] * len(series))
    for index, row in enumerate(series):
        # TODO remove str function
        soup = BeautifulSoup(markup=string_parser(str(row)), features='lxml')
        addresses[index] = soup.find('span', class_='street-address').text
        cities[index] = soup.find('span', class_='locality').text
    return addresses, cities


def decode_working_time(results: Tuple[Tuple[str, str, str]]) -> dict:
    """
    Decode results from WorkingTime table
    :param results: results ((place_id, days, time), ) from WorkingTime table
    :return:
    """
    wt = WorkingTime()
    dict_ = dict()
    for item in results:
        key = item[0]
        if dict_.get(key):
            dict_[key].update(days=item[1], time=item[2])
        else:
            dict_[key] = wt.decode(days=item[1], time=item[2])
    return dict_


def string_parser(query: str):
    """
    Parse the query to find the collections in it
    :param query: string to parse
    :return: collection
    """
    pattern = r'^\[(?P<list_>.*)\]$'
    result = re.search(pattern, query)
    if result:
        if not result.group('list_').startswith('\'<'):  # in case if query is html code like <span id="1">text</span>
            return json.loads(
                '{"text": ' + result.group('list_').replace('\'', '"').replace('"[', '[').replace(']"', ']')
                + ' , "status" : "OK"}', encoding='utf-8',
            )['text']
        else:
            return result.group('list_')
    return query


def get_value(x: str, first: bool = True):
    """
    Get collection from json query
    :param x: json query
    :param first: if it is a list return the first element
    :return: collection
    """
    # TODO remove str function
    x = string_parser(str(x))
    if type(x) is list and first:
        return x[0]
    return x


if __name__ == '__main__':
    data = read_parquet(path=os.path.join(REQUESTS_DIR, 'places.parquet'))
    df = transform_df_to_places(data=data, columns_dict=DB_PLACES_COLUMNS)
    print(df.head())
    # df = transform_df_to_working_time(data=data, columns_dict=DB_WORKING_TIME_COLUMNS)
    # print(df.head())
