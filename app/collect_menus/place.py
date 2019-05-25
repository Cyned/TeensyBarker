from config import MENUS_DIR
from collect_menus.utils import get_filename_from_url
from collect_menus.file_saver import FileSaver
from collect_menus.place_page import PlacePage
from app import parser_logger as logger


class Place(object):
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
                    f'{page.parse_url.calls} urls were parsed. '
                    f'Menus pages count: {len(menu_pages) + len(menu_images)}'
                    )
        for image in menu_images:
            try:
                self.saver.save_url(path=image, file_name=get_filename_from_url(url=image))
            except Exception as e:
                logger.error(e)

        for page in menu_pages:
            try:
                self.saver.save_pdf(url=page, file_name=get_filename_from_url(url=page))
            except Exception as e:
                logger.error(e)
