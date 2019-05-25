import requests
import json

from typing import Tuple

from config import GOOGLE_API_KEY
from app import collect_logger as logger


def places_nearby_search(*, location: Tuple[float, float], type_: str, radius: int, page_token: str = '',
                         language: str = 'en-AU', min_price: int = 0, max_price: int = 4,
                         open_now: bool = False) -> dict:
    """
    Search all places in radius from current location via GoogleMaps API
    :param location: coordinates of the epicenter of the search
    :param type_: type of place to search
    :param radius: radius of the search
    :param page_token: token of the page
    :param language: language of the search
    :param min_price: min price of the place
    :param max_price: max price of the place
    :param open_now: if the place is open now
    :return: result data dictionary from GoogleMaps
    """

    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?' \
          'location={location}&radius={radius}&type={type}&language={language}&minprice={min_price}' \
          '&maxprice={max_price}&opennow={open_now}&key={APIKEY}{pagetoken}'.format(
        location=','.join(map(str, location)), radius=radius, type=type_, language=language,
        min_price=min_price, max_price=max_price, open_now=open_now, APIKEY=GOOGLE_API_KEY,
        pagetoken="&pagetoken=" + page_token if page_token else "",
    )

    logger.debug(f'Response url: {url}')
    response = requests.get(url)
    res = json.loads(response.text)
    try:
        obj = res['results']
    except KeyError:
        logger.warning('Invalid response for request: {}'.format(res['status']))
        return {}
    return obj


def place_details(*, place_id: str, page_token: str = '') -> dict:
    """
    Search details about the place via GoogleMaps API
    :param place_id: id of the place
    :param page_token: token of the page
    :return: result data dictionary from GoogleMaps
    """

    url = 'https://maps.googleapis.com/maps/api/place/details/json?placeid={placeid}&key={APIKEY}{pagetoken}'.format(
        placeid=place_id, APIKEY=GOOGLE_API_KEY, pagetoken="&pagetoken=" + page_token if page_token else "",
    )
    logger.debug(f'Response url: {url}')
    response = requests.get(url)
    res = json.loads(response.text)
    try:
        obj = res['result']
    except KeyError:
        logger.warning('Invalid response for place_id: {}. {}'.format(place_id, res['status']))
        return {}
    return obj


def place_find(*, text: str, language: str = 'en-AU', location_bias: str = 'point:90,90', input_: str = 'restaurant',
               fields: Tuple[str, str] = ('geometry', 'id'), page_token: str = '') -> dict:
    """
    :param text:
    :param language: language of the search
    :param location_bias:
    :param input_:
    :param fields:
    :param page_token: token of the page
    :return: result data dictionary from GoogleMaps
    """

    url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?' \
          'language={lang}&inputtype={text}&locationbias={location_bias}&input={input}&fields={fields}' \
          '&key={APIKEY}{pagetoken}'.format(
        lang=language, text=text, location_bias=location_bias, input=input_, fields=','.join(fields),
        APIKEY=GOOGLE_API_KEY, pagetoken="&pagetoken=" + page_token if page_token else "",
    )
    logger.debug(f'Response url: {url}')
    response = requests.get(url)
    logger.info(response.text)
    res = json.loads(response.text)
    try:
        obj = res['result']
    except KeyError:
        logger.warning('Invalid response. {}'.format(res['status']))
        return {}
    return obj


def places_text_search(*, query: str, location: Tuple[float, float], language: str = 'en-AU',
                       max_price: int = 4, min_price: int = 1, open_now: bool = False,
                       radius: int = 1000, type_: str = 'restaurant', page_token: str = '') -> dict:
    """

    :param query:
    :param location: coordinates of the epicenter of the search
    :param language: language of the search
    :param max_price: max price of the place
    :param min_price: min price of the place
    :param open_now: if the place is open now
    :param radius: radius of the search
    :param type_: type of place to search
    :param page_token: token of the page
    :return: result data dictionary from GoogleMaps
    """

    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?' \
          'language={lang}&location={location}&maxprice={max_price}&minprice={min_price}&opennow={open_now}' \
          '&query={query}&radius={radius}type={type}&key={APIKEY}{pagetoken}'.format(
        lang=language, location=','.join(map(str, location)), max_price=max_price, min_price=min_price,
        open_now='true' if open_now else 'false', query=query, radius=radius, type=type_,
        APIKEY=GOOGLE_API_KEY, pagetoken="&pagetoken=" + page_token if page_token else "",
    )
    logger.debug(f'Response url: {url}')
    response = requests.get(url)
    logger.info(response.text)
    res = json.loads(response.text)
    try:
        obj = res['results']
    except KeyError:
        logger.warning('Invalid response. {}'.format(res['status']))
        return {}
    return obj


def places_radar_search(*, keyword: str, location: Tuple[float, float], name: str = 'bar',
                        max_price: int = 4, min_price: int = 1, open_now: bool = False,
                        radius: int = 1000, type_: str = 'restaurant', page_token: str = '') -> dict:
    """

    :param keyword:
    :param location: coordinates of the epicenter of the search
    :param name:
    :param max_price: max price of the place
    :param min_price: min price of the place
    :param open_now: if the place is open now
    :param radius: radius of the search
    :param type_: type of place to search
    :param page_token: token of the page
    :return: result data dictionary from GoogleMaps
    """

    url = 'https://maps.googleapis.com/maps/api/place/radarsearch/json?' \
          'keyword={keyword}&location={location}&maxprice={max_price}&minprice={min_price}' \
          '&name={name}&opennow={open_now}&radius={radius}type={type}&key={APIKEY}{pagetoken}'.format(
        keyword=keyword, location=','.join(map(str, location)), max_price=max_price, min_price=min_price,
        name=name, open_now='true' if open_now else 'false', radius=radius, type=type_,
        APIKEY=GOOGLE_API_KEY, pagetoken="&pagetoken=" + page_token if page_token else "",
    )
    logger.debug(f'Response url: {url}')
    response = requests.get(url)
    logger.info(response.text)
    res = json.loads(response.text)
    try:
        obj = res['results']
    except KeyError:
        logger.warning('Invalid response. {}'.format(res['status']))
        return {}
    return obj
