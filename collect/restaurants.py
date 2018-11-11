from urllib.request import urlopen
from urllib.parse import unquote
from bs4 import BeautifulSoup
from requests import get as http_get
from os import path, makedirs
import time


class RestaurantLogger:
    """Logging restaurant processing process"""
    def __init__(self):
        """Init timer variables and iterator"""
        self.before = None
        self.after = None
        self.iteration = 1

    def start(self):
        """Start timer to calculate execution time"""
        self.before = time.time()

    def log(self, current_url, menu_urls, used_urls, to_be_processed):
        """Log all necessary info about parsing process"""
        print("""
===========
==== """ + str(self.iteration) + """ ====
===========
        """)
        print("  {} {}\n".format("Parsing", current_url))

        print("  Found menu URLs on page:")
        if not menu_urls:
            print("    <None>")
        elif type(menu_urls) is list:
            for url in menu_urls:
                print("    -", url)
        else:
            print("    -", menu_urls)

        print("\n  Parsed URLs:")
        if not used_urls:
            print("    <None>")
        elif type(used_urls) is list:
            for url in used_urls:
                print("    -", url)
        else:
            print("    -", used_urls)

        print("\n  To be processed:")
        if not to_be_processed:
            print("    <None>")
        elif type(to_be_processed) is list:
            for url in to_be_processed:
                print("    -", url)
        else:
            print("    -", to_be_processed)

        self.iteration += 1

    def end(self):
        """After done with parsing whole site - show parsing time"""
        self.after = time.time()
        print("\n\n{} {} {}\n"
              .format(
                "Working time is",
                round(self.after-self.before, 1),
                "sec"))


class RestaurantPage:
    """Looks for menu images or pdf files on the restaurant page"""
    def __init__(self, site_url, url, used_urls=[]):
        """Init some useful values"""
        self.SITE_URL = site_url
        self.IMAGE_FORMATS = [".pdf", ".jpg", ".jpeg", ".png", ".bmp", ".tiff"]
        self.MENU = ["menyu", "menu"]
        self.DISHES = [
            "вино", "вина", "винная", "винна", "салати", "салаты", "напої",
            "напитки", "соки"]
        self.directory = "./data/"+self.get_foldername_from_url(self.SITE_URL)
        self.url = url  # current url
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
        return url[url.rfind('/')+1:]

    def get_foldername_from_url(self, url):
        """Get name of the folder from the website url"""
        url = url[url.find("://")+3:]  # url without http:// or https://
        return url[:url.find("/")]

    def save_file_from_url(self, m_url, filename):
        """Saves file from url"""
        req = http_get(m_url)

        # If folder not exists - create
        if not path.exists(self.directory):
            makedirs(self.directory)

        with open(self.directory + "/" + filename, "wb") as f:
            f.write(req.content)

        self.used_urls.append(m_url)

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
        self.used_urls.append(self.url)

        # If self.url is a menu image - save it
        if self.is_image_link(self.url):
            print("\n  Downloading image", self.url)
            filename = self.get_filename_from_url(self.url)
            self.save_file_from_url(self.url, filename)
            return

        try:
            html = urlopen(self.url)
            self.bs = BeautifulSoup(html.read(), features="lxml")
        except:
            return

        self.search_menu_urls()


class Restaurant:
    """Looks for menu images (or pdf files) on the whole restaurant website"""
    def __init__(self, site_url, current_url):
        """Init restaurant url"""
        self.site_url = site_url
        self.current_url = current_url

    def collect_menu(self):
        """Find all menu images on the restaurant website and download them"""
        urls = [self.current_url]
        used_urls = []
        logger = RestaurantLogger()
        logger.start()

        for url in urls:
            page = RestaurantPage(self.site_url, url, used_urls)
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
