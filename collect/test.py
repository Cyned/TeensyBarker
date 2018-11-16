import unittest
import tempfile
import os
import shutil

from restaurants import Restaurant


def get_foldername_from_url(url):
    """Get name of the folder from the website url"""
    url = url[url.find("://")+3:]  # url without http:// or https://
    return url[:url.find("/")]

def finding_menus(url):
    """Get all filenames from test and template folders"""
    testdir = "test"
    fortestdir = "fortest"
    test_content = []
    fortest_content = []

    try:
        restaurant = Restaurant(url, testdir)
        restaurant.collect_menu()

        foldername = get_foldername_from_url(url)
        test_content = os.listdir(testdir + "/" + foldername)
        fortest_content = os.listdir(fortestdir + "/" + foldername)

    finally:
        shutil.rmtree(testdir)

    return test_content, fortest_content


class SiteTests(unittest.TestCase):
    """Test finding menu on the different websites"""

    def test_santori(self):
        """
        img & pdf
        Test finding menu on the site http://santori.com.ua/
        """
        url = "http://santori.com.ua/"
        test_content, fortest_content = finding_menus(url)
        self.assertEqual(test_content, fortest_content)

    def test_mistercat(self):
        """
        img & pdf
        Test finding menu on the site https://mistercat.ua/
        """
        url = "https://mistercat.ua/"
        test_content, fortest_content = finding_menus(url)
        self.assertEqual(test_content, fortest_content)

    def test_finefamily(self):
        """
        html
        Test finding menu on the site http://finefamily.com.ua/
        """
        url = "http://finefamily.com.ua/"
        test_content, fortest_content = finding_menus(url)
        self.assertEqual(test_content, fortest_content)


if __name__ == "__main__":
    unittest.main()
