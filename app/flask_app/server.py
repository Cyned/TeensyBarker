from flask import request, send_file, Response

from flask_app.utils import get_menu_from_place
from flask_app import app
from app import app_logger as logger


@app.route('/menu', methods=['GET'])
def get_menu():
    """ Send menu of the place to download """
    place = request.headers['place']
    menu_paths = get_menu_from_place(place_name=place)

    try:
        return send_file(menu_paths, attachment_filename='menu.pdf')
    except Exception as e:
        logger.exception(e)

    return Response(status=404)
