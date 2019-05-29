import random

import numpy as np

from os.path import join as path_join
from typing import Callable, List, Set, Tuple
from functools import wraps
from nltk.tokenize import word_tokenize

from databases import DBPlaces
from config import MENUS_DIR
from app import lemmatizer, app_logger as logger
from flask_app import error_message


def limiter(func: Callable) -> Callable:
    """ Decorator randomly choose one item from the returning list of the function"""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Tuple[str, float]:
        """ Wrapper of decorator """
        results, score = func(*args, **kwargs)
        random.seed(3413)
        return random.choice(results), score
    return wrapper


@limiter
def get_menu_from_place(place_name: str) -> Tuple[List[str], float]:
    """
    Get path to the menu of the place
    :param place_name: name of the place to search menu of
    :return: full path to the menu file, probability of searched place
    """
    score = 1.0
    with DBPlaces() as db:
        place_id = db.get_place_from_name(place_name=place_name.lower())
        if not place_id:
            logger.info(f'There is no exact match. Go into the relative search of {place_name}')
            all_places = db.get_places(['name'])
            place_name, score = get_most_probably_name(need_place=place_name, places=[x[0] for x in all_places])
            if score == 0.0:
                return [], score
            place_id = db.get_place_from_name(place_name=place_name)
        menus = db.get_menus_from_place_id(place_id=place_id)
    return [path_join(MENUS_DIR, str(place_id), menu_file) for menu_file in menus], score


def get_detailed_info(place_name: str) -> Tuple[dict, float]:
    """
    GEt detailed information from the database about the place
    :param place_name: name of the place to search
    :return: detailed information fro the database, probability of searched place
    """
    score = 1.0
    with DBPlaces() as db:
        info = db.get_info_place_from_name(place_name=place_name.lower())
        if not info:
            logger.info(f'There is no exact match. Go into the relative search of {place_name}')
            all_places = db.get_places(['name'])
            place_name, score = get_most_probably_name(need_place=place_name, places=[x[0] for x in all_places])
            if score == 0.0:
                return {}, score
            info = db.get_info_place_from_name(place_name=place_name)
    return info, score


def get_all_places() -> List[str]:
    """ Returns all places from the database """
    with DBPlaces() as db:
        places = db.get_places(columns='name')
    return [place_sample[0] for place_sample in places]


def tokenize(text: str) -> Set[str]:
    """
    Tokenize text. Filter numbers and spec symbols
    :param text: text to tokenize
    :return: list of words from the text
    """
    return {lemmatizer.lemmatize(word) for word in word_tokenize(text=text.lower())}


def get_most_probably_name(need_place: str, places: List[str]) -> Tuple[str, float]:
    """
    Get the most nearest place from the `places` list to needful place
    :param need_place: name of place we need
    :param places: list of places to search throw
    :return: name of the most nearest place, and its proximity
    """
    need_place_toks = tokenize(need_place)
    scores = np.zeros(len(places))
    for ix, place in enumerate(places):
        place_toks = tokenize(text=place)
        scores[ix] = 2 * len(need_place_toks & place_toks) / (len(need_place_toks) + len(place_toks))
    return places[np.argmax(scores, axis=0)], np.max(scores)


def unexpected_error(func: Callable):
    """ Catch all unexpected errors in the application """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            logger.exception(e)
        return error_message('Internal server error.')
    return wrapper
