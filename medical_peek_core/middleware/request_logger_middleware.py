import logging

from medical_peek_core.middleware.core_middleware import HookMiddleware

logger = logging.getLogger(__name__)


class RequestLogMiddleware(HookMiddleware):
    # noinspection PyMethodMayBeStatic
    def process_request(self, request):
        """
        Provides additional logging information for all requests coming into the Django Server. This includes the
        username, type of HTTP request, and requested URI.

        If the user is available, then the username of the user is included in the log. Otherwise, the username
        is set to 'Anonymous' and included in the log.

        :param request:
        :type request: django.http.HttpRequest
        :return:
        :rtype:
        """
        if not hasattr(request, 'user') or request.user.is_anonymous():
            user = 'Anonymous'
        else:
            user = request.user.username
        logger.info(f'User {user} making {request.method} request for {request.path}')
        return None
