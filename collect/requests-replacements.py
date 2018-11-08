import requests
from urllib.request import urlopen
from urllib.parse import unquote
from bs4 import BeautifulSoup

# url = "http://santori.com.ua/uf/Menu/menubar/Sets%20A3_04.jpg"
url = "http://santori.com.ua/menyu/festivalnoe-menyu/"

req = requests.get(url)
real_url = unquote(req.url)

print("url:", url)
print("Real url:", real_url)
