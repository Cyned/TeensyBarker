import os
from waitress import serve

from flask_app import app, server
from config import HOST, PORT


if __name__ == '__main__':
    serve(
        app,
        host=os.environ.get('HOST', HOST),
        port=os.environ.get('PORT', PORT),
        expose_tracebacks=True,
    )
