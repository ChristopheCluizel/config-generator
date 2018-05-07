class ApiException(Exception):
    def __init__(self, exception_message="", api_message="", class_instance=None):
        self.exception_message = exception_message
        self.api_message = api_message
        self.class_instance = class_instance


class Exception_400(ApiException):
    def __init__(self, exception_message, api_message, class_instance):
        ApiException.__init__(self, exception_message, api_message, class_instance)


class Exception_404(ApiException):
    def __init__(self, exception_message, api_message, class_instance):
        ApiException.__init__(self, exception_message, api_message, class_instance)
