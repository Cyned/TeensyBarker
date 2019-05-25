from config import MENUS_DIR
from collect_menus.utils import get_filename_from_url
from collect_menus.file_saver import FileSaver
from collect_menus.place_page import PlacePage
from databases import BDPlaces
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

        with BDPlaces() as db:
            for image in menu_images:
                try:
                    file_name = get_filename_from_url(url=image)
                    self.saver.save_url(path=image, file_name=file_name)
                    self.save_to_db(db=db, file_name=file_name, place_id=self.place_id)
                except Exception as e:
                    logger.error(e)

            for page in menu_pages:
                try:
                    file_name = get_filename_from_url(url=page)
                    self.saver.save_pdf(url=page, file_name=file_name)
                    self.save_to_db(db=db, file_name=file_name, place_id=self.place_id)
                except Exception as e:
                    logger.error(e)

    @staticmethod
    def save_to_db(db, file_name: str, place_id: str):
        """
        Save to the database link to the file
        :param file_name: path to the file
        :param db: path to the file
        :param place_id: id of the menu
        """
        res = db.get_menus(file_name=file_name)
        if res:
            # in case file name is already exists in the database we should update date
            db.execute(f"""update "Menus" set "DateMenuUpdated" = current_timestamp where "MenuId" = '{res[0][0]}';""")
        else:
            # Not in the database => save filepath & DateMenuUpdated
            db.execute('insert into "Menus"' +
                       ' ("PlaceId", "MenuLinkToFS", "DateMenuUpdated")' +
                       ' values (' +
                       place_id + ', \'' + file_name + '\', current_timestamp);')
