from django.conf.urls import url
from user.views import *

urlpatterns = [
    url(r'^login/?$', UserLogin.as_view()),
    url(r'^logout/?$', UserLogout.as_view()),
    url(r'^apply/list?$', ApplyList.as_view()),
    url(r'^create/question/?$', CreateQuestion.as_view()),
    url(r'^create/section/?$', CreateSection.as_view()),
    url(r'^create/form/?$', CreateForm.as_view()),
    url(r'^handle/apply/?$', HandleApply.as_view()),
    url(r'^check/form/?$', CheckForm.as_view()),
    url(r'^check/formbase?$', CheckFormBase.as_view()),
    url(r'^check/sectionbase?$', CheckSectionBase.as_view()),
    url(r'^check/questionbase?$', CheckQuestionBase.as_view()),
    url(r'^formbase/list?$', FormBaseList.as_view()),
    url(r'^sectionbase/list?$', SectionBaseList.as_view()),
    url(r'^questionbase/list?$', QuestionBaseList.as_view()),
]