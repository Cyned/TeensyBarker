from lxml import html
import requests


class Restaurants:
    """Collect menus from restaurants urls"""
    def __init__(self):
        self.urls = []

    def load_urls(self):
        with open('./urls.txt', 'r') as f:
            lines = f.readlines()
            self.urls = [url.replace('\n', '') for url in lines]

    def parse_website(self, url):
        page = requests.get(url)
        tree = html.fromstring(page.content)
        print(tree)


def main():
    restaurants = Restaurants()
    # restaurants.load_urls()
    restaurants.parse_website('http://santori.com.ua')


if __name__ == "__main__":
    main()
