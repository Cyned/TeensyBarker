import re
import json

import pandas as pd
import numpy as np

from bs4 import BeautifulSoup

from config import DB_PLACES_COLUMNS, DB_WORKING_TIME_COLUMNS
from working_time import WorkingTime


def transform_df_to_places(data: pd.DataFrame, columns_dict: dict):
    """
    Transform DataFrame to needful view for the Places table

    :param data: pandas.DataFrame with GoogleMaps API information
    :type data: pd.DataFrame
    :param columns_dict: dictionary where values are the columns in current database
    :type columns_dict: dict
    :return: dictionary for Places table
    """

    results = dict()
    columns = {
        columns_dict['name']:     'name',
        columns_dict['website']:  'website',
        columns_dict['address']:  'nan',  # we do not need to parse these object
        columns_dict['city']:     'nan',  # we do not need to parse these object
        columns_dict['place_id']: 'reference',
        columns_dict['loc_x']:    'geometry_location_lng',
        columns_dict['loc_y']:    'geometry_location_lat',
        columns_dict['phone']:    'international_phone_number',
    }
    for key, value in columns.items():
        if value in data.columns:
            results[key] = list(data[value].apply(get_value))
        else:
            results[key] = [None] * data.shape[0]
    if 'adr_address' in data.columns:
        results[columns_dict['address']], results[columns_dict['city']] = get_address(data['adr_address'])
    if columns[columns_dict['phone']] in data.columns:
        results[columns_dict['phone']] = [x.replace(' ', '').replace('+', '') for x in results[columns_dict['phone']]]
    return list(zip(*results.values()))


def transform_df_to_working_time(data: pd.DataFrame, place_ids, columns_dict: dict):
    """
    Transform DataFrame to needful view for the WorkingTime table

    :param data: pandas.DataFrame with GoogleMaps API information
    :type data: pd.DataFrame
    :param place_ids: ((reference, place_id(in Places table), ...)
    :type place_ids: tuple
    :param columns_dict: dictionary where values are the columns in current database
    :type columns_dict: dict
    :return: dictionary for WorkingTime table
    """

    dict_ = dict(place_ids)
    new_data = data[['reference', 'opening_hours_weekday_text']]
    new_data['place_id'] = new_data['reference'].apply(lambda x: dict_.get(get_value(x)))

    results = dict()
    wt = WorkingTime()
    wt.parse(
        ids=new_data['place_id'],
        times=[get_value(tmp, first=False) for tmp in new_data['opening_hours_weekday_text'].values],
    )
    if wt.ids:
        results[columns_dict['place_id']] = wt.ids
        results[columns_dict['days']] = list(map(int, wt.days))
        results[columns_dict['open_time']] = wt.time
    else:
        return None
    return list(zip(*results.values()))


def delete_existed(data: pd.DataFrame, columns: tuple, results: tuple):
    """
    Delete from current data records that columns have results values

    :param data: data from GoogleMaps API request
    :param columns: columns to compare
    :type columns: tuple
    :param results: values to delete in data
    :type results: tuple
    :return: new pd.DataFrame
    """

    if not columns or not results:
        raise ValueError('Empty attributes')
    results = tuple(zip(*results))
    if len(columns) != len(results):
        raise ValueError('Columns and results attributes have to be one shape.')

    if len(columns) == 1:
        df = data.loc[
            ~data[columns[0]].apply(lambda x: get_value(x) in results[0])
        ]
    else:
        df = data.loc[~np.logical_and(
            *[data[columns[index]].apply(lambda x: get_value(x) in results[index]) for index in range(len(results))]
        )]

    return df


def get_address(serie: pd.Series):
    """
    Parse html to get address and city of each item of serie.

    :param serie: pandas.Series object; HTML with address information
    :return: two numpy.array
    """

    addresses = np.array([None] * len(serie))
    cities = np.array([None] * len(serie))
    for index, row in enumerate(serie):
        # TODO remove str function
        soup = BeautifulSoup(string_parser(str(row)))
        addresses[index] = soup.find('span', class_='street-address').text
        cities[index] = soup.find('span', class_='locality').text
    return addresses, cities


def decode_working_time(results):
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
    :type query: str
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


def get_value(x, first: bool=True):
    """
    Get collection from json query

    :param x: json query
    :type x: str
    :param first: if it is a list return the first element
    :type first: bool
    :return: collection
    """

    # TODO remove str function
    x = string_parser(str(x))
    if type(x) is list and first:
        return x[0]
    return x


if __name__ == '__main__':
    # data = pd.read_csv('../data/places.csv')
    # df = transform_df_to_places(data=data, columns_dict=DB_PLACES_COLUMNS)
    # print(df)

    data = pd.read_csv('../data/khreschatyk_new.csv')
    df = transform_df_to_working_time(data, DB_WORKING_TIME_COLUMNS)
    print(df)
    pass
