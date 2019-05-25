import re

from urllib.parse import urlparse
from typing import List, Iterable, Tuple
from nltk.stem import WordNetLemmatizer
from functools import wraps

from constants import IMAGE_FORMATS, MENU_NAMES
from config import DISHES


lemmatizer = WordNetLemmatizer()


def is_image_link(url: str) -> bool:
    """
    Checks if provided url is an image
    :param url: url
    """
    for format_ in IMAGE_FORMATS:
        if url.endswith(format_):
            return True
    return False


def is_menu_link(url: str) -> bool:
    """
    Checks is provided url is a menu link
    :param url:
    """
    words_in_url = tokenize_url(url=url)
    for format_ in MENU_NAMES + DISHES:
        if format_ in words_in_url:
            return True
    return False


def get_filename_from_url(url: str) -> str:
    """
    Get name of the file from provided url
    :param url: url
    """
    host, path = get_host(path=url)
    return path.replace('/', '_')


def tokenize_url(url: str) -> List:
    """
    Tokenize url
    :param url: url to tokenize
    :return: words in url
    """
    if not url.startswith('http'):
        url = 'http://' + url
    parsed = urlparse(url)
    return [lemmatizer.lemmatize(word) for word in re.split(r'[\.?\-\/]+', parsed.path[1:] + parsed.query)]


# def save_to_db(file_path: str, place_id: str):
#     """
#     Save to the database link to the file
#     :param file_path: path to the file
#     :param place_id: id of the menu
#     """
#     with BDPlaces() as db:
#         res = db.execute('select "MenuId" from "Menus" where "MenuLinkToFS" = \'' +
#                          file_path + '\';')
#
#         if res:
#             # File path is already in the database => update DateMenuUpdated
#             menu_id = str(res[0][0])
#             db.execute('update "Menus" set "DateMenuUpdated" = current_timestamp' +
#                        ' where "MenuId" = \'' + menu_id + '\';')
#         else:
#             # Not in the database => save filepath & DateMenuUpdated
#             db.execute('insert into "Menus"' +
#                        ' ("PlaceId", "MenuLinkToFS", "DateMenuUpdated")' +
#                        ' values (' +
#                        place_id + ', \'' + file_path + '\', current_timestamp);')


def find_all_relative_urls(content: str) -> List[str]:
    """
    Find all urls in the web page
    :param content: html content of the web page
    :return: list of urls
    """
    return [url[1] for url in re.findall(r'(src|href)="(?P<url>/[^"]*)"', content, flags=re.IGNORECASE) if url]


def replace_with_host(urls: Iterable, host: str, content: str) -> str:
    """
    Replace all relative urls (from `urls`) in the content into the absolute paths
    :param urls: list of urls in the content to replace
    :param host: domain name of the web site
    :param content: html content of the web page
    :return: new html source
    """
    for url in urls:
        content = content.replace(f'"{url}"', f'{host}{url}')
    return content


def get_host(path: str) -> Tuple[str, str]:
    """
    Get host and path of the url
    :param path: url to parse
    :return: netloc and path of the url

    'http://localhost:9000/google.com/about/?search' -> ('localhost:9000', '/google.com/about/')
    'http://google.com/about/?search'                -> ('google.com', '/about/')
    """
    if not path.startswith('http'):
        path = 'http://' + path
    parsed = urlparse(path)
    return parsed.netloc, parsed.path


def count_calls(func):
    """ Count the calls of function `func` """
    @wraps(func)
    def wrapper(*args, **kwargs):
        """ Increment count value of the function `func` """
        wrapper.calls += 1
        return func(*args, **kwargs)
    wrapper.calls = 0
    return wrapper


if __name__ == '__main__':
    print(is_menu_link(url='http://www.puzatahata.ua/restaurants/dnipropetrovsk'))
