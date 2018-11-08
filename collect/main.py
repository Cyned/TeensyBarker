from restaurants import Restaurant
import time


def main():
    url = "http://santori.com.ua/"
    before = time.time()

    restaurant = Restaurant(url)
    restaurant.collect_menu()

    after = time.time()
    print("\n\n{} {} {}\n"
        .format("Working time is", round(after-before, 1), "sec"))


if __name__ == "__main__":
    main()
