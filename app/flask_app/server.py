from flask import request, send_file, jsonify, Response

from flask_app.utils import get_menu_from_place, get_detailed_info, get_all_places, unexpected_error
from flask_app import app, error_message
from app import app_logger as logger


@unexpected_error
@app.route('/', methods=['GET'])
def test():
    return 'Here we are!'


@unexpected_error
@app.route('/menu', methods=['GET'])
def get_menu():
    """ Send menu of the place to download """
    place = request.headers.get('place')
    if not place:
        return error_message('Not params get')
    logger.info(f'Get menu of {place}')
    menu_path, score  = get_menu_from_place(place_name=place)
    logger.info(f'Score: {score*100:.2f}%')
    if score != 0.0:
        try:
            return send_file(menu_path, attachment_filename='menu.pdf')
        except Exception as e:
            logger.exception(e)
    else:
        return error_message('There is no such a place.')
    return error_message('Internal server error.')


@unexpected_error
@app.route('/place', methods=['GET'])
def get_place():
    """ Get detailed information about the place """
    place = request.headers.get('place')
    if not place:
        return error_message('Not params get')
    logger.info(f'Get detailed info about {place}')
    place_info, score = get_detailed_info(place_name=place)
    logger.info(f'Score: {score*100:.2f}%')
    if score != 0.0:
        return jsonify(dict(status='success', **place_info))
    else:
        return error_message('There is no such a place.')
    return error_message('Internal server error.')


@app.route('/places', methods=['GET'])
def get_places():
    """ Send menu of the place to download """
    places = get_all_places()
    logger.info('Get all places from the database')
    return jsonify({'status': 'success', 'places': places})
