class BasePostgres(object):

    def __init__(self):
        self.conn = None

    def add(self, **kwargs):
        raise AttributeError()

    def remove(self, *args, **kwargs):
        raise AttributeError()

    def check_is_in(self, *args, **kwargs):
        raise AttributeError()

    def get(self, *args, **kwargs):
        raise AttributeError()
