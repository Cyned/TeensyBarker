from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import os


def is_image_link(url):
    for format in IMAGE_FORMATS:
        if url.endswith(format):
            return True
    return False


def is_menu_link(url):
    for format in MENU:
        if url.lower().find(format) != -1:
            return True
    return False


def get_filename_from_url(url):
    return url[url.rfind('/')+1:]


def get_foldername_from_url(url):
    url = url[url.find("://")+3:] #  url without http:// or https://
    return url[:url.find("/")]


def save_file_from_url(m_url, directory, filename):
    req = requests.get(m_url)

    # If folder not exists - create
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(directory + "/" + filename, "wb") as f:
        f.write(req.content)


# Get menu links
def get_menu_urls():
    menu_urls = []
    links = bsObj.findAll("a")  # look for all links

    for link in links:
        # If a tag has no href - skip it
        try:
            m_url = link["href"]
        except KeyError as e:
            continue
        # Remove first slash if needed
        if m_url[:1] == '/':
            m_url = m_url[1:]


        if is_menu_link(m_url):
            menu_urls.append(SITE_URL + m_url)

    # Remove duplicates
    menu_urls = list(set(menu_urls))

    return menu_urls

def save_menu_images(menu_urls):
    menu_urls_copy = menu_urls[:]
    # used_urls = []
    for i in range(len(menu_urls_copy)):
        m_url = menu_urls_copy[i]
        # If url is to file - save it
        if is_image_link(m_url):
            print("Image URL:", m_url)
            filename = get_filename_from_url(m_url)
            save_file_from_url(m_url, directory, filename)
            menu_urls.remove(m_url)  # remove used links from urls list
            # ... add used urs to appropriate list


def is_bsObj_pdf_file(url):
    try:
        return bsObj.p.get_text().find("[/PDF/Text/ImageB/ImageC/ImageI]") != -1
    except:
        return False


SITE_URL = "http://santori.com.ua/"
directory = "./data/" + get_foldername_from_url(SITE_URL)
# url = "http://santori.com.ua/menyu/menyu-bara/"  # current url
url = "http://santori.com.ua/menyu/menyu-bara/bar/"
IMAGE_FORMATS = [".pdf", ".jpg", ".jpeg"]
MENU = ["menyu", "menu"]

html = urlopen(url)
bsObj = BeautifulSoup(html.read(), features="lxml")

menu_urls = get_menu_urls()

print("Menu: ")
for menu_url in menu_urls:
    print(menu_url)

save_menu_images(menu_urls)

print("Menu: ")
for menu_url in menu_urls:
    print(menu_url)

if is_bsObj_pdf_file(bsObj):
    url = url[:-1] #  url without last slash
    filename = url[url.rfind("/")+1:] + ".pdf"
    save_file_from_url(url, directory, filename)
