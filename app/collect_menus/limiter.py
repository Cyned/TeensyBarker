import random

from config import MAX_MENU_PAGES
from collect_menus.utils import count_calls


def MaxMenuPages(cls):
    """
    Decorator to prevent over parsing of pages. It overwrites `parse_url` method.
    :param cls: `PlaceBase` class
    """

    @count_calls
    def parse_url(self, *args, **kwargs):
        """ Overrides `parse_url` method """
        if len(self.menu_pages) + len(self.menu_images) < MAX_MENU_PAGES:
            return parse_url_method(self, *args, **kwargs)
        return

    def drop(self):
        """ Drop menu urls from `menu_pages` and `-images`. Preference is given to `menu_pages` """
        if len(self._menu_pages) + len(self._menu_images) > MAX_MENU_PAGES:
            if len(self._menu_pages) > MAX_MENU_PAGES:
                random.seed(375)
                self._menu_pages = set(random.sample(self._menu_pages, MAX_MENU_PAGES))
                self._menu_images = set()
            if len(self._menu_pages) == 0:
                if len(self._menu_images) > MAX_MENU_PAGES:
                    random.seed(375)
                    self._menu_images = set(random.sample(self._menu_images, MAX_MENU_PAGES))
            else:
                rest = MAX_MENU_PAGES - len(self._menu_pages)
                if len(self._menu_images) > rest:
                    random.seed(375)
                    self._menu_images = set(random.sample(self._menu_images, rest))

    @property
    def menu_pages(self):
        """ Returns `menu_pages` previously dropping its """
        drop(self)
        return self._menu_pages

    @property
    def menu_images(self):
        """ Returns `menu_images` previously dropping its """
        drop(self)
        return self._menu_images

    parse_url_method = cls.parse_url

    cls.parse_url    = parse_url
    cls.menu_pages   = menu_pages
    cls.menu_images  = menu_images

    return cls
