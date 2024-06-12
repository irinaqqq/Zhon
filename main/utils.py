from django.utils.timezone import now
from .models import UserSession

def get_total_time_spent(user):
    sessions = UserSession.objects.filter(user=user)
    total_time = 0
    for session in sessions:
        if session.logout_time:
            total_time += (session.logout_time - session.login_time).total_seconds() / 60  # duration in minutes
        else:
            total_time += (now() - session.login_time).total_seconds() / 60  # if the user is still logged in
    return int(total_time)
