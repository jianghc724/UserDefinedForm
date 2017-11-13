from django.conf.urls import url
from user.views import *

urlpatterns = [
    url(r'^login/?$', UserLogin.as_view()),
    url(r'^logout/?$', UserLogout.as_view()),
    url(r'^apply/list?$', FormList.as_view()),
    url(r'^create/question?$', CreateQuestion.as_view()),
    url(r'^create/section?$', CreateSection.as_view()),
    url(r'^create/form?$', CreateForm.as_view()),
    url(r'^handle/apply?$', HandleApply.as_view()),
    url(r'^check/apply?$', CheckForm.as_view()),
    url(r'^check/form?$', CheckFormBase.as_view()),
    url(r'^check/section?$', CheckSectionBase.as_view()),
    url(r'^check/question?$', CheckQuestionBase.as_view()),
    url(r'^form/list?$', FormBaseList.as_view()),
    url(r'^section/list?$', SectionBaseList.as_view()),
    url(r'^question/list?$', QuestionBaseList.as_view()),
]