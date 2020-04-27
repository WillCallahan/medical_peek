class HookMiddleware(object):
    """
    Middleware with default __init__ and __call__ methods so that hooks can easily be implemented
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response
