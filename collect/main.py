from restaurants import Restaurant


def main():
    # url = "http://santori.com.ua/"
    # url = "http://dumka.kiev.ua/menu/"
    # url = "https://mistercat.ua/"
    site_url = "http://finefamily.com.ua/uk/menyu.html"
    url = "http://finefamily.com.ua/"

    restaurant = Restaurant(site_url, url)
    restaurant.collect_menu()


if __name__ == "__main__":
    main()
