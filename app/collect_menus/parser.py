import threading
import requests

from bs4 import BeautifulSoup
from typing import List

from collect_menus.utils import find_all_relative_urls, replace_with_host, get_host
from app import parser_logger as logger


class Parser(object):

    __bs_lock = threading.Lock()

    def __init__(self, url: str):
        """
        :param url: url to parse
        """
        if not url.startswith('http'):
            url = 'http://' + url
        self._url  : str = url
        self._host : str = ''

        try:
            content = requests.get(self.url).content.decode('utf-8', errors='ignore')
        except Exception as e:
            logger.error(e)
            raise e

        self.host, _ = get_host(path=self.url)
        content = replace_with_host(
            urls=find_all_relative_urls(content=content),
            host=self.host, content=content,
        )

        with self.__bs_lock:
            self._bs = BeautifulSoup(content, features="lxml")

            # to display hidden elements
            # htmlfile = self._bs.prettify().replace("display: none", "display: block")
            logger.debug(f'parsed {self.url}')

    @property
    def url(self) -> str:
        """ Return url """
        return self._url

    @property
    def host(self) -> str:
        """ Return url """
        return self._host

    @host.setter
    def host(self, host: str):
        """ Return url """
        if host:
            self._host = host

    def get_links(self) -> List:
        """ Get links from the web site """
        return [link['href'] for link in self._bs.findAll(name="a") if link.get('href') and self.host in link['href']]

    def get_images(self) -> List:
        """ Get all images from the web site """
        return [link['src'] for link in self._bs.findAll(name="img") if link.get('src') and self.host in link]
