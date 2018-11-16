from restaurants import Restaurant


def main():
    # url = "http://santori.com.ua/"
    # url = "https://mistercat.ua/"
    # url = "http://finefamily.com.ua/"

    restaurant = Restaurant(url)
    restaurant.collect_menu()


if __name__ == "__main__":
    main()
