import unittest
import tempfile
import os
import shutil

from restaurants import Restaurant


class SiteTests(unittest.TestCase):
    """Test finding menu on the different websites"""

    def __init__(self, *args, **kwargs):
        """"""
        super(SiteTests, self).__init__(*args, **kwargs)
        self.testdir = "test"
        self.fortestdir = "fortest"
        self.test_content = []
        self.fortest_content = []

    def setUp(self):
        """Clear temp variables after each test"""
        self.test_content = []
        self.fortest_content = []

    def finding_menus(self, url):
        """Get all filenames from test and template folders"""
        restaurant = Restaurant(url, self.testdir)
        restaurant.collect_menu()

        foldername = self.get_foldername_from_url(url)
        self.test_content = os.listdir(self.testdir + "/" + foldername)
        self.fortest_content = os.listdir(self.fortestdir + "/" + foldername)

    def get_foldername_from_url(self, url):
        """Get name of the folder from the website url"""
        url = url[url.find("://")+3:]  # url without http:// or https://
        return url[:url.find("/")]

    @unittest.skip('always skipped')
    def test_santori(self):
        """
        img & pdf
        Test finding menu on the site http://santori.com.ua/
        """
        url = "http://santori.com.ua/"
        self.finding_menus(url)
        self.assertEqual(self.test_content, self.fortest_content)

    @unittest.skip('always skipped')
    def test_mistercat(self):
        """
        img & pdf
        Test finding menu on the site https://mistercat.ua/
        """
        url = "https://mistercat.ua/"
        self.finding_menus(url)
        self.assertEqual(self.test_content, self.fortest_content)

    @unittest.skip('always skipped')
    def test_finefamily(self):
        """
        html
        Test finding menu on the site http://finefamily.com.ua/
        """
        url = "http://finefamily.com.ua/"
        self.finding_menus(url)
        self.assertEqual(self.test_content, self.fortest_content)

    def test_nikala(self):
        """
        html
        Test finding menu on the site http://nikala.kiev.ua/
        """
        url = "http://nikala.kiev.ua/"
        self.finding_menus(url)
        self.assertEqual(self.test_content, self.fortest_content)

    @unittest.skip('always skipped')
    def test_cimes(self):
        """
        php
        Test finding menu on the site http://www.cimes.com.ua/
        """
        url = "http://www.cimes.com.ua/"
        self.finding_menus(url)
        self.assertEqual(self.test_content, self.fortest_content)

    def tearDown(self):
        """Delete test directory"""
        shutil.rmtree(self.testdir)


if __name__ == "__main__":
    unittest.main()
