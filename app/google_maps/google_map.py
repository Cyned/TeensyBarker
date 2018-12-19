import requests
import json

import logging as logger

from app.config import GOOGLE_API_KEY


def places_nearby_search(location, type_, radius, page_token=None, language='en-AU',
                         min_price=0, max_price=4, open_now=False):
    """
    Search all places in radius from current location via GoogleMaps API
    :return: dict
    """

    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?' \
          'location={location}' \
          '&radius={radius}' \
          '&type={type}' \
          '&language={language}' \
          '&minprice={min_price}' \
          '&maxprice={max_price}' \
          '&opennow={open_now}' \
          '&key={APIKEY}{pagetoken}'.format(location=','.join(map(str, location)),
                                            radius=radius,
                                            type=type_,
                                            language=language,
                                            min_price=min_price,
                                            max_price=max_price,
                                            open_now=open_now,
                                            APIKEY=GOOGLE_API_KEY,
                                            pagetoken="&pagetoken=" + page_token if page_token else "",
                                            )
    logger.info(f'Response url: {url}')
    response = requests.get(url)
    res = json.loads(response.text)
    try:
        obj = res['results']
    except KeyError:
        logger.warning('Invalid response for request: {}'.format(res['status']))
        return None
    return obj


def place_details(place_id, page_token=None):
    """
    Search details about the place via GoogleMaps API
    :return: dict
    """

    url = 'https://maps.googleapis.com/maps/api/place/details/json?' \
          'placeid={placeid}' \
          '&key={APIKEY}{pagetoken}'.format(placeid=place_id,
                                            APIKEY=GOOGLE_API_KEY,
                                            pagetoken="&pagetoken=" + page_token if page_token else "",
                                            )
    logger.info(f'Response url: {url}')
    response = requests.get(url)
    res = json.loads(response.text)
    try:
        obj = res['result']
    except KeyError:
        logger.warning('Invalid response for place_id: {}. {}'.format(place_id, res['status']))
        return None
    return obj


def place_find(text, language='en-AU', location_bias='point:90,90', input_='restaurant',
               fields=('geometry', 'id'), page_token=None):
    """

    :return: dict
    """

    url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?' \
          'language={lang}' \
          '&inputtype={text}' \
          '&locationbias={location_bias}' \
          '&input={input}' \
          '&fields={fields}' \
          '&key={APIKEY}{pagetoken}'.format(lang=language,
                                            text=text,
                                            location_bias=location_bias,
                                            input=input_,
                                            fields=','.join(fields),
                                            APIKEY=GOOGLE_API_KEY,
                                            pagetoken="&pagetoken=" + page_token if page_token else "",
                                            )
    logger.info(f'Response url: {url}')
    response = requests.get(url)
    logger.info(response.text)
    res = json.loads(response.text)
    try:
        obj = res['result']
    except KeyError:
        logger.warning('Invalid response. {}'.format(res['status']))
        return None
    return obj


def places_text_search(query, location, language='en-AU', max_price=4, min_price=1, open_now=False,
                       radius=1000, type_='restaurant', page_token=None):
    """
    For experiments
    :return: dict
    """

    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?' \
          'language={lang}' \
          '&location={location}' \
          '&maxprice={max_price}' \
          '&minprice={min_price}' \
          '&opennow={open_now}' \
          '&query={query}' \
          '&radius={radius}' \
          'type={type}' \
          '&key={APIKEY}{pagetoken}'.format(lang=language,
                                            location=','.join(map(str, location)),
                                            max_price=max_price,
                                            min_price=min_price,
                                            open_now='true' if open_now else 'false',
                                            query=query,
                                            radius=radius,
                                            type=type_,
                                            APIKEY=GOOGLE_API_KEY,
                                            pagetoken="&pagetoken=" + page_token if page_token else "",
                                            )
    logger.info(f'Response url: {url}')
    response = requests.get(url)
    logger.info(response.text)
    res = json.loads(response.text)
    try:
        obj = res['results']
    except KeyError:
        logger.warning('Invalid response. {}'.format(res['status']))
        return None
    return obj


def places_radar_search(keyword, location, name='bar', max_price=4, min_price=1, open_now=False,
                        radius=1000, type_='restaurant', page_token=None):
    """
    For experiments
    :return: dict
    """

    url = 'https://maps.googleapis.com/maps/api/place/radarsearch/json?' \
          'keyword={keyword}' \
          '&location={location}' \
          '&maxprice={max_price}' \
          '&minprice={min_price}' \
          '&name={name}' \
          '&opennow={open_now}' \
          '&radius={radius}' \
          'type={type}' \
          '&key={APIKEY}{pagetoken}'.format(keyword=keyword,
                                            location=','.join(map(str, location)),
                                            max_price=max_price,
                                            min_price=min_price,
                                            name=name,
                                            open_now='true' if open_now else 'false',
                                            radius=radius,
                                            type=type_,
                                            APIKEY=GOOGLE_API_KEY,
                                            pagetoken="&pagetoken=" + page_token if page_token else "",
                                            )
    logger.info(f'Response url: {url}')
    response = requests.get(url)
    logger.info(response.text)
    res = json.loads(response.text)
    try:
        obj = res['results']
    except KeyError:
        logger.warning('Invalid response. {}'.format(res['status']))
        return None
    return obj
