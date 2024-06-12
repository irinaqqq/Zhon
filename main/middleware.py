import datetime
from django.utils.timezone import now
from .models import UserSession

class UserSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_request(self, request):
        if request.user.is_authenticated:
            UserSession.objects.create(user=request.user, login_time=now())

    def process_response(self, request, response):
        if request.user.is_authenticated and not request.user.is_anonymous:
            try:
                user_session = UserSession.objects.filter(user=request.user).latest('login_time')
                user_session.logout_time = now()
                user_session.save()
            except UserSession.DoesNotExist:
                pass
        return response
