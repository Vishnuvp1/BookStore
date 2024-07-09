import logging

logger = logging.getLogger(__name__)


class LogRequestMiddleware:
    """
    Middleware to log the HTTP method and path of incoming requests.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info(f"Request Method: {request.method}, Request Path: {request.path}")
        response = self.get_response(request)
        return response
