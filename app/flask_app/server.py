from flask_app import app


@app.route('/', methods=['GET'])
def test():
    return 'test success'
