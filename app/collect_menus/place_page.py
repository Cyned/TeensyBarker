from typing import Set, Tuple

from collect_menus.utils import is_menu_link, is_image_link, count_calls
from collect_menus.parser import Parser
from collect_menus.limiter import MaxMenuPages


class PageBase(object):
    @property
    def menu_images(self) -> set:
        raise NotImplemented

    @property
    def menu_pages(self) -> set:
        raise NotImplemented

    def parse_url(self, *args, **kwargs):
        raise NotImplemented

    def collect_menu(self, *args, **kwargs) -> Tuple[Set[set], Set[set]]:
        raise NotImplemented


@MaxMenuPages
class Page(PageBase):
    """ Looks for menu images or pdf files on the restaurant page """

    def __init__(self, website: str):
        """
        :param website: web site to parse
        """
        self._website     : str = website
        self._menu_pages  : set = set()  # all menu urls from web site
        self._menu_images : set = set()  # all images url from web site
        self.used_urls    : set = set()  # urls that are already checked for menus

    @property
    def menu_pages(self) -> Set[str]:
        """ Get menu_urls list """
        return self._menu_pages

    @property
    def menu_images(self) -> Set[str]:
        """ Get menu_urls list """
        return self._menu_images

    @property
    def website(self) -> str:
        """ Get website """
        return self._website

    @count_calls
    def parse_url(self, url: str):
        """
        Get all menu links found on the page
        :param url: url to parse to find menus
        """
        try:
            parser = Parser(url=url)
            self.used_urls.add(url)
        except Exception:
            return
        url_to_parse = []
        for link in parser.get_links() + parser.get_images():
            if is_menu_link(link) and link not in self.menu_pages:
                if is_image_link(link):
                    self.menu_images.add(link)
                else:
                    self.menu_pages.add(link)
            elif link not in self.used_urls:
                url_to_parse.append(link)
            continue

        # parse url deeper
        for url in url_to_parse:
            self.parse_url(url=url)

    def collect_menu(self) -> Tuple[Set[str], Set[str]]:
        """
        Finds all menu images on the page and downloads them
        :return: set of the menu urls
        """
        self.parse_url(url=self.website)
        return self.menu_pages, self.menu_images
