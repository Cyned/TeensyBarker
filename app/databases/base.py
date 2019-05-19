class BasePostgres(object):

    def __init__(self):
        self.conn = None

    def add(self, **kwargs):
        raise NotImplementedError

    def get(self, *args, **kwargs):
        raise NotImplementedError

    def execute(self, *args, **kwargs):
        raise NotImplementedError
