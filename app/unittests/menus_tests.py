import unittest
import os
import shutil

from os.path import join as path_join

from collect_menus.places import Place


class SiteTests(unittest.TestCase):
    """ Test finding menu on the different web sites """

    def __init__(self, *args, **kwargs):
        """"""
        super(SiteTests, self).__init__(*args, **kwargs)
        self.test_dir         : str  = "test"
        self.for_test_dir     : str  = "for_test"
        self.test_content     : list = []
        self.for_test_content : list = []

    def set_up(self):
        """ Clear temporal variables after each test """
        self.test_content     = []
        self.for_test_content = []

    def find_menus(self, url: str):
        """ Get all filenames from test and template folders """
        restaurant = Place(url, self.test_dir)
        restaurant.collect_menu()

        folder_name = self.get_folder_name_from_url(url)
        self.test_content     = os.listdir(path_join(self.test_dir, folder_name))
        self.for_test_content = os.listdir(path_join(self.for_test_dir, folder_name))

    @staticmethod
    def get_folder_name_from_url(url: str):
        """ Get name of the folder from the website url """
        url = url[url.find("://")+3:]  # url without http:// or https://
        return url[:url.find("/")]

    def test_santori(self):
        """
        img & pdf
        Test finding menu on the site http://santori.com.ua/
        """
        url = "http://santori.com.ua/"
        self.find_menus(url=url)
        self.assertEqual(self.test_content, self.for_test_content)

    def test_mistercat(self):
        """
        img & pdf
        Test finding menu on the site https://mistercat.ua/
        """
        url = "https://mistercat.ua/"
        self.find_menus(url)
        self.assertEqual(self.test_content, self.for_test_content)

    def test_finefamily(self):
        """
        html
        Test finding menu on the site http://finefamily.com.ua/
        """
        url = "http://finefamily.com.ua/"
        self.find_menus(url=url)
        self.assertEqual(self.test_content, self.for_test_content)

    def test_nikala(self):
        """
        html
        Test finding menu on the site http://nikala.kiev.ua/
        """
        url = "http://nikala.kiev.ua/"
        self.find_menus(url)
        self.assertEqual(self.test_content, self.for_test_content)

    def test_cimes(self):
        """
        php
        Test finding menu on the site http://www.cimes.com.ua/
        """
        url = "http://www.cimes.com.ua/"
        self.find_menus(url)
        self.assertEqual(self.test_content, self.for_test_content)

    def tear_down(self):
        """Delete test directory"""
        shutil.rmtree(self.test_dir)


if __name__ == "__main__":
    unittest.main()
