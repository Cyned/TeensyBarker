import sys

from flask import Flask

from config import APP_DIR


app = Flask(__name__)

sys.path.append(APP_DIR)
