from django.conf.urls import url
from user.views import *

urlpatterns = [
    # url(r'^user/register/?$', UserRegister.as_view()),
    url(r'^login/?$', UserLogin.as_view()),
    url(r'^apply/list?$', ApplyList.as_view()),
    url(r'^question/?$', CreateQuestion.as_view()),
    url(r'^section/?$', CreateSection.as_view()),
    url(r'^form/?$', CreateForm.as_view()),
    url(r'^rate/?$', HandleApply.as_view()),
]