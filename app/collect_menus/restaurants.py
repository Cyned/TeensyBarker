import pdfkit

from bs4 import BeautifulSoup
from os import path, makedirs
from urllib.request import urlopen
from urllib.parse import unquote
from requests import get as http_get

from logger import RestaurantLogger
from config import MENUS_DIR
from databases import BDPlaces


class RestaurantPage:
    """Looks for menu images or pdf files on the restaurant page"""
    def __init__(self, site_url, url, used_urls=[], dirname=MENUS_DIR,
            subdirname=None):
        """Init some useful values"""
        self.SITE_URL = site_url
        self.IMAGE_FORMATS = [".pdf", ".jpg", ".jpeg", ".png", ".bmp", ".tiff"]
        self.MENU = ["menyu", "menu", "kitchen"]
        # self.DISHES = [
        #     "вино", "вина", "винная", "винна", "салати", "салаты", "напої",
        #     "напитки", "соки", "закуски", "блюда", "гарниры", "соусы",
        #     "десерты", "course", "garnish", "desserts", "pastry", "salads",
        #     "sauces", "snacks", "wine", "alcohol", "drinks"]
        self.placeid = subdirname

        if subdirname:
            self.directory = dirname + "/" + subdirname
        else:
            self.directory = dirname + "/" + \
                self.get_foldername_from_url(self.SITE_URL)

        self.URL = url  # current url
        self.bs = None  # BeautifulSoup object
        self.menu_urls = []  # all menu urls from site
        self.used_urls = used_urls  # list of processed urls

    def get_menu_urls(self):
        """Get menu_urls list"""
        return self.menu_urls

    def get_used_urls(self):
        """Get used_urls list"""
        return self.used_urls

    def is_with_http(self, url):
        """Checks if url starts with http:// or https://"""
        prefixes = ["http://", "https://"]
        for prefix in prefixes:
            if url.find(prefix) != -1:
                return True
        return False

    def is_image_link(self, url):
        """Checks is provided url is an image"""
        for format in self.IMAGE_FORMATS:
            if url.endswith(format):
                return True
        return False

    def is_menu_link(self, url):
        """Checks is provided url is a menu link"""
        for format in self.MENU:
            if url.lower().find(format) != -1:
                return True
        return False

    def get_filename_from_url(self, url):
        """Get name of the file from provided url"""
        if url[-1:] == "/":
            url = url[:-1]
        return url[url.rfind("/")+1:]

    def get_foldername_from_url(self, url):
        """Get name of the folder from the website url"""
        url = url[url.find("://")+3:]  # url without http:// or https://
        return url[:url.find("/")]

    def get_php_filename(self, url):
        """
        Extract php filename from ulr
        Ex.: http://www.cimes.com.ua/main.php?open=kitchen&cat=1 => /main.php
        """
        return url[url.rfind("/"):url.find(".php")+4]

    def save_file_from_url(self, m_url, filename):
        """Saves file from url"""
        req = http_get(m_url)

        # If folder not exists - create
        if not path.exists(self.directory):
            makedirs(self.directory)

        filepath = self.directory + "/" + filename

        with open(filepath, "wb") as f:
            f.write(req.content)

        # Add link to the file to the database
        if self.placeid:
            self.saveToDatabase(filepath)

        self.used_urls.append(m_url)

    def saveToDatabase(self, filepath):
        """Save to the database link to the file"""
        with BDPlaces() as db:
            res = db.execute('select "MenuId" from "Menus" where "MenuLinkToFS" = \'' +
                filepath + '\';')

            if res:
                # Filepath is already in the database => update DateMenuUpdated
                menuid = str(res[0][0])
                db.execute('update "Menus" set "DateMenuUpdated" = current_timestamp' +
                    ' where "MenuId" = \'' + menuid + '\';')
            else:
                # Not in the database => save filepath & DateMenuUpdated
                db.execute('insert into "Menus"' +
                ' ("PlaceId", "MenuLinkToFS", "DateMenuUpdated")' +
                ' values (' +
                str(self.placeid) + ', \'' + filepath + '\', current_timestamp);')

    # Get menu links
    def search_menu_urls(self):
        """Get all menu links found on the page"""
        links = list(set(self.bs.findAll("a")))  # look for all links
        images = list(set(self.bs.findAll("img")))  # look for all images

        for link in links:
            # If has no href tag - skip it
            try:
                m_url = link["href"]
            except:
                continue

            if self.is_menu_link(m_url):
                url = m_url
                if not self.is_with_http(url):
                    # Remove first slash if needed
                    if url[:1] == '/':
                        url = url[1:]

                    # Add sitename if url is just params to php site
                    # Ex.: ?page=3 => http://www.site.com/main.php?page=3
                    if url[0] == "?":
                        php_filename = self.get_php_filename(self.URL)
                        url = self.SITE_URL + php_filename + url
                    else:
                        url = self.SITE_URL + url

                if url not in self.used_urls:
                    self.menu_urls.append(url)

        for img in images:
            # If has no src tag - skip it
            try:
                img_url = img["src"]
            except:
                continue

            if self.is_menu_link(img_url):
                url = img_url
                if not self.is_with_http(url):
                    # Remove first slash if needed
                    if url[:1] == '/':
                        url = url[1:]
                    url = self.SITE_URL + url
                if url not in self.used_urls:
                    self.menu_urls.append(url)

        self.menu_urls = list(set(self.menu_urls))  # remove duplicates

    def collect_menu(self):
        """Find all menu images on the page and download them"""
        # Add url to the used urls list
        self.used_urls.append(self.URL)

        filename = self.get_filename_from_url(self.URL)
        if self.is_image_link(self.URL):
            # If self.URL is a menu image - save it
            self.save_file_from_url(self.URL, filename)
            return

        try:
            html = urlopen(self.URL).read()
            self.bs = BeautifulSoup(html, features="lxml")
        except:
            return

        # Make a pdf from the url which is not website homepage
        if self.URL != self.SITE_URL:

            # If folder not exists - create
            if not path.exists(self.directory):
                makedirs(self.directory)

            # Generate filename for the pdf file
            filename = filename.replace(".html", "")  # TEMP SOLUTION => TO BE REPLACED!!!
            filepath = self.directory + "/" + filename + ".pdf"
            htmlfile = self.bs.prettify()  # html.decode('utf-8')

            # Show all hidden elements (could be menu items)
            htmlfile = htmlfile.replace("display: none", "display: block")
            htmlfile = htmlfile.replace("display:none", "display: block")

            # Save pdf options
            options = {
                "quiet": ""
            }

            try:
                # Save pdf
                pdfkit.from_url(self.URL, filepath, options=options)

                # Add link to the file to the database
                if self.placeid:
                    self.saveToDatabase(filepath)
            except:
                pass

        self.search_menu_urls()


class Restaurant:
    """Looks for menu images (or pdf files) on the whole restaurant website"""
    def __init__(self, site_url, dirname=MENUS_DIR, subdirname=None):
        """Init restaurant url"""
        self.site_url = site_url
        self.dirname = dirname
        self.subdirname = subdirname

    def collect_menu(self):
        """Find all menu images on the restaurant website and download them"""
        urls = [self.site_url]
        used_urls = []
        logger = RestaurantLogger()
        logger.start()

        for url in urls:
            page = RestaurantPage(self.site_url, url, used_urls, self.dirname,
                self.subdirname)
            page.collect_menu()

            menu_urls = page.get_menu_urls()

            for menu_url in menu_urls:
                try:
                    req = http_get(menu_url)
                    real_url = unquote(req.url)
                except:
                    continue
                if real_url not in urls and real_url not in used_urls:
                    urls.append(real_url)

            # Logging
            to_be_processed = urls
            logger.log(url, menu_urls, used_urls, to_be_processed)

        logger.end()
