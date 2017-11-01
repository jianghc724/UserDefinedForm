from django.conf.urls import url
from user.views import *

urlpatterns = [
    url(r'^user/register/?$', UserRegister.as_view()),
    url(r'^user/login/?$', UserLogin.as_view()),
]