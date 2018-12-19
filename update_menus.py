import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'app/'))
# print(os.path.join(os.getcwd(), 'app/'))

from collect_menus import Restaurant
from databases import BDPlaces


def update_menus():
    """ Update menus data """

    # Process websites one by one
    with BDPlaces() as db:
        results = db.execute('select "PlaceId", "Website" from "Places";')

        for placeid, website in results:
            # if website:
            if website == "http://orlypark.com.ua/":
                placeid = str(placeid)
                restaurant = Restaurant(website, subdirname=placeid)
                restaurant.collect_menu()


if __name__ == "__main__":
    update_menus()
