from restaurants import Restaurant
from database.database import execute


def main():
    # url = "http://santori.com.ua/"
    # url = "https://mistercat.ua/"
    # url = "http://finefamily.com.ua/"
    # url = "http://nikala.kiev.ua/"
    # url = "http://www.cimes.com.ua/"

    # restaurant = Restaurant(url)
    # restaurant.collect_menu()

    # Get all urls from the database
    results = execute('select "Website" from "Places"')

    # Process websites one by one
    for result in results:
        website = result[0]
        print(website)
        # restaurant = Restaurant(website)
        # restaurant.collect_menu()


if __name__ == "__main__":
    main()
