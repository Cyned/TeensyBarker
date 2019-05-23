import requests
from typing import Set, Tuple

from config import MENUS_DIR
from collect_menus.utils import is_menu_link, get_filename_from_url
from collect_menus.parser import Parser
from collect_menus.file_saver import FileSaver
from app import parser_logger as logger


class PlacePage:
    """Looks for menu images or pdf files on the restaurant page"""

    def __init__(self, website: str):
        """
        :param website: web site to parse
        """
        self._website     : str = website
        self._menu_pages   : set = set()  # all menu urls from web site
        self._menu_images : set = set()  # all images url from web site
        self.used_urls    : set = set()  # urls that are already checked for menus

    @property
    def menu_pages(self) -> set:
        """ Get menu_urls list """
        return self._menu_pages

    @property
    def menu_images(self) -> set:
        """ Get menu_urls list """
        return self._menu_images

    @property
    def website(self) -> str:
        """ Get website """
        return self._website

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
        url_to_parse = set()
        for link in parser.get_links():
            if is_menu_link(link) and link not in self.menu_pages:
                self.menu_pages.add(link)
            elif link not in self.used_urls:
                url_to_parse.add(link)
            continue

        for img in parser.get_images():
            if is_menu_link(img) and img not in self.menu_images:
                self.menu_images.add(img)
            continue
        # parse url deeper
        for url in url_to_parse:
            self.parse_url(url=url)

    def collect_menu(self) -> Tuple[Set[set], Set[set]]:
        """
        Finds all menu images on the page and downloads them
        :return: set of the menu urls
        """
        self.parse_url(url=self.website)
        return self.menu_pages, self.menu_images


class Place:
    """ Class that looks for menu images (or pdf files) on the website """

    def __init__(self, website: str, place_id: str = MENUS_DIR):
        """
        :param website: website to parse
        :param place_id: id of the place
        """
        self._website  = website
        self._place_id = place_id

        self.saver = FileSaver(dirname=place_id)

    @property
    def website(self):
        """ Returns website """
        return self._website

    @property
    def place_id(self):
        """ Returns website """
        return self._place_id

    def collect_menu(self):
        """ Find all menu images / documents on the place website and download them """
        page = PlacePage(website=self.website)
        menu_pages, menu_images = page.collect_menu()

        logger.info(f'Url {self.website}. '
                    # f'{Parser.count} urls were parsed. '
                    f'Menus pages count: {len(menu_pages) + len(menu_images)}'
                    )

        for page in menu_images:
            try:
                response = requests.get(url=page)
            except Exception:
                continue
            self.saver.save_content(content=response.content, file_name=get_filename_from_url(url=page))

        for image in menu_images:
            self.saver.save_pdf(url=image, file_name=get_filename_from_url(url=image))
