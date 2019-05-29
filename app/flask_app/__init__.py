import sys

from flask import Flask, jsonify

from config import APP_DIR


app = Flask(__name__)

sys.path.append(APP_DIR)

error_message = lambda msg: jsonify({'status': 'fail', 'message': msg})
