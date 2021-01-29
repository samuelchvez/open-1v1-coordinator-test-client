class Resource(object):
    def __init__(self, endpoint, path):
        self.endpoint = endpoint
        self.path = path
        self.token = None
        self.is_auth = False

    def authorize(self, token):
        self.is_auth = True
        self.token = token

    def build_url(self, action=''):
        return f'{self.endpoint}/{self.path}/{action}'
