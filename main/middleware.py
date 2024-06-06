# import time
# from django.utils.deprecation import MiddlewareMixin
# from .models import UserSession

# class SessionDurationMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         if request.user.is_authenticated:
#             request.session['session_start_time'] = time.time()

#     def process_response(self, request, response):
#         if request.user.is_authenticated and 'session_start_time' in request.session:
#             session_start_time = request.session['session_start_time']
#             session_end_time = time.time()
#             duration = session_end_time - session_start_time
#             UserSession.objects.create(user=request.user, duration=duration)
#             del request.session['session_start_time']
#         return response
