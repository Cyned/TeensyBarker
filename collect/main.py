from restaurants import Restaurant
from database.database import execute


def main():
    # url = "http://santori.com.ua/"
    # url = "https://mistercat.ua/"
    # url = "http://finefamily.com.ua/"
    # url = "http://nikala.kiev.ua/"
    # url = "http://www.cimes.com.ua/"
    # url = "http://orlypark.com.ua/"
    #
    # restaurant = Restaurant(url)
    # restaurant.collect_menu()

    # Get all urls from the database
    # results = execute('select * from "Places"')
    placeid = execute("""INSERT INTO "Places"
        ("Name", "Website", "Address", "City", "GooglePin", "CoordinateX", "CoordinateY")
        values
            (\'name\', \'website\', \'address\', \'city\', \'pin\', 1, 1) returning "PlaceId";
        """)

    print(placeid)

    # res = execute('select * from "Places" where "PlaceId" = 2;')
    # print(res)

    # Process websites one by one
    # for result in results:
    #     website = result[0]
    #     print(website)
        # restaurant = Restaurant(website)
        # restaurant.collect_menu()


if __name__ == "__main__":
    main()
