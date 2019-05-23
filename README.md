# TeensyBarker collector

Utility for collect menus from websites.


# Getting Started

1. Make sure you have **Python >=3.7.0** and **pip** for appropriate Python version. Also ypu will need wkhtmltopdf==0.12.4-1
2. Install all requirements via following command
```
pip3 install -r requirements.txt
```

# Connect to the database

To test database connection create a file **database/database.ini** with following content
```
[postgresql]
host=<hostname>
database=<database>
user=<username>
password=<password>
```

# Test

```
python3 test.py
```
