# TeensyBarker collector

Utility for collect menus and other needful data from places.


## Getting Started

1. Make sure you have **Python >=3.7.0** and **pip** for appropriate Python version.
2. Install all requirements via following commands:
    ```
    pip3 install -r requirements.txt
    sudo apt install wkhtmltopdf=0.12.4-1
    ```
3. You will need also to download some `nltk` data. Go to __python__ console and follow these commands:
    ```
    impprt nltk
    nltk.download('wordnet')
    ```

## Connect to the database

To test database connection create a file `app/database/database.ini` with following content
```
[postgresql]
host=<hostname>
database=<database>
user=<username>
password=<password>
```

## Test if all is going well

```
python3 test.py
```

## Run updaters

To run places and menu updaters you need run these python modules:
```
./app/udpdate_places.py
./app/udpdate_menus.py
```
