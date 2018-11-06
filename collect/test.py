from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import os


def is_picture_link(url):
    for format in PICTURE_FORMATS:
        if len(url) - url.find(format) == len(format):
            return True
    return False


def get_filename_from_url(url):
    return url[url.rfind('/')+1:]


def get_foldername_from_url(url):
    return url[url.find("://")+3:-1]


def save_file_from_url(m_url, url):
    req = requests.get(m_url)
    directory = "./data/" + get_foldername_from_url(url)
    filename = directory + "/" + get_filename_from_url(m_url)

    # If folder not exists - create
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(filename, "wb") as f:
        f.write(req.content)


url = "http://santori.com.ua/"
PICTURE_FORMATS = [".pdf", ".jpg", ".jpeg"]
html = urlopen(url)
bsObj = BeautifulSoup(html.read(), features="lxml")

links = bsObj.findAll("a")  # look for all links
menu_urls = []

# Get menu links
for link in links:
    if link.get_text().lower().find("меню") != -1:
        m_url = link["href"]
        if m_url[:1] == '/':
            m_url = m_url[1:]
        menu_urls.append(url + m_url)

# Remove duplicates
menu_urls = list(set(menu_urls))

for m_url in menu_urls:
    # If url is to file - save it
    if is_picture_link(m_url):
        print(m_url)
        save_file_from_url(m_url, url)
