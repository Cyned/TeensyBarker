from restaurants import Restaurant
from database.database import execute


def main():
    # url = "http://santori.com.ua/"
    # url = "https://mistercat.ua/"
    # url = "http://finefamily.com.ua/"
    # url = "http://nikala.kiev.ua/"
    # url = "http://www.cimes.com.ua/"
    # url = "http://orlypark.com.ua/"
    # url = "http://www.sushi24.ua/"

    # restaurant = Restaurant(url)
    # restaurant.collect_menu()

    results = execute('select "PlaceId", "Website" from "Places";')

    # Process websites one by one
    for result in results:
        placeid = str(result[0])
        website = result[1]
        if website:
            if website == "http://orlypark.com.ua/":
                restaurant = Restaurant(website, subdirname=placeid)
                restaurant.collect_menu()


if __name__ == "__main__":
    main()
