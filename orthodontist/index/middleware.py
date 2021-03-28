import datetime
from django.core.cache import cache
from orthodontist import settings
from django.utils.deprecation import MiddlewareMixin


class ActiveUserMiddleware(MiddlewareMixin):

    def process_request(self, request):
        current_user = request.user
        if current_user.is_authenticated:
            now = datetime.datetime.now()
            cache.set(f'seen_{current_user.username}', now, settings.USER_LASTSEEN_TIMEOUT)