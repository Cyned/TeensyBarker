import random

from os.path import join as path_join
from typing import Callable, List
from functools import wraps

from databases import DBPlaces
from config import MENUS_DIR


def limiter(func: Callable) -> Callable:
    """ Decorator randomly choose one item from the returning list of the function"""
    @wraps(func)
    def wrapper(*args, **kwargs) -> str:
        """ Wrapper of decorator """
        results = func(*args, **kwargs)
        random.seed(3413)
        return random.choice(results)
    return wrapper


@limiter
def get_menu_from_place(place_name: str) -> List[str]:
    """
    Get path to the menu of the place
    :param place_name: name of the place to search menu of
    :return: full path to the menu file
    """
    with DBPlaces() as db:
        place_id = db.get_place_from_name(place_name=place_name)
        menus = db.get_menus_from_place_id(place_id=place_id)
    return [path_join(MENUS_DIR, str(place_id), menu_file) for menu_file in menus]
