class APIException(Exception):
    def __init__(self, message, code=None):
        self.context = {}
        if code:
            self.context['errorCode'] = code
        super().__init__(message)