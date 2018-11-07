from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import os


class RestaurantPage:
    """Looks for menu images or pdf files on the restaurant page"""
    def __init__(self, site_url, url, used_urls=[]):
        """Init some useful values"""
        self.SITE_URL = site_url
        self.IMAGE_FORMATS = [".pdf", ".jpg", ".jpeg"]
        self.MENU = ["menyu", "menu"]
        self.directory = "./data/"+self.get_foldername_from_url(self.SITE_URL)
        self.url = url  # current url
        self.bs = None  # BeautifulSoup object
        self.menu_urls = []  # all menu urls from site
        self.used_urls = used_urls  # list of processed urls

    def print_menu_urls(self):
        """Display menu_urls list"""
        print("Menu: ")
        for menu_url in self.menu_urls:
            print(menu_url)

    def is_image_link(self, url):
        """Checks is provided url is an image or pdf"""
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
        req = requests.get(m_url)

        # If folder not exists - create
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        with open(self.directory + "/" + filename, "wb") as f:
            f.write(req.content)

    # Get menu links
    def search_menu_urls(self):
        """Get all menu links found on the page"""
        links = self.bs.findAll("a")  # look for all links

        for link in links:
            # If a tag has no href - skip it
            try:
                m_url = link["href"]
            except KeyError as e:
                continue
            # Remove first slash if needed
            if m_url[:1] == '/':
                m_url = m_url[1:]

            if self.is_menu_link(m_url):
                url = self.SITE_URL + m_url
                if url not in self.used_urls:
                    self.menu_urls.append(url)

        # Remove duplicates
        self.menu_urls = list(set(self.menu_urls))

    def save_menu_images(self):
        """Found all urls to files from urls list and save these files"""
        menu_urls_copy = self.menu_urls[:]
        # used_urls = []
        for i in range(len(menu_urls_copy)):
            m_url = menu_urls_copy[i]
            # If url is to file - save it
            if self.is_image_link(m_url):
                print("Image URL:", m_url)
                filename = self.get_filename_from_url(m_url)
                self.save_file_from_url(m_url, filename)
                # Remove used links from urls list
                self.menu_urls.remove(m_url)
                # Add processed urls to appropriate list
                self.used_urls.append(m_url)

        # Whole website is pdf file - save it
        if self.is_bs_pdf_file():
            print("PDF URL:", self.url)
            url = self.url[:-1]  # url without last slash
            filename = url[url.rfind("/")+1:] + ".pdf"
            self.save_file_from_url(self.url, filename)
            # Add processed urls to appropriate list
            self.used_urls.append(self.url)

    def is_bs_pdf_file(self):
        """Checks is current page object is pdf file"""
        try:
            pdf_pattern = "[/PDF/Text/ImageB/ImageC/ImageI]"
            return self.bs.p.get_text().find(pdf_pattern) != -1
        except Exception:
            return False
            raise

    def collect_menu(self):
        """Find all menu images on the page and download them"""
        print("\n\nProcessing ...", self.url)
        html = urlopen(self.url)
        self.bs = BeautifulSoup(html.read(), features="lxml")

        self.search_menu_urls()
        # self.print_menu_urls()
        self.save_menu_images()
        # self.print_menu_urls()

    def get_menu_urls(self):
        """Get menu_urls list"""
        return self.menu_urls

    def get_used_urls(self):
        """Get used_urls list"""
        return self.used_urls


class Restaurant:
    """Looks for menu images or pdf files on the whole restaurant website"""
    def __init__(self, site_url):
        """Init restaurant url"""
        self.site_url = site_url

    def collect_menu(self):
        """Find all menu images on the restaurant website and download them"""
        urls = [self.site_url]
        used = []
        count = 1

        for url in urls:
            print("\n\n\n============" + str(count) + "============\n\n")
            page = RestaurantPage(self.site_url, url, used)
            page.collect_menu()

            menu_urls = page.get_menu_urls()
            used = page.get_used_urls()

            print("Menu:", menu_urls, end="\n\n")
            print("URLs list:", urls, end="\n\n")
            print("Used:", used, end="\n\n")

            for menu_url in menu_urls:
                if menu_url not in urls:
                    urls.append(menu_url)

            count += 1
