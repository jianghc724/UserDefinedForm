from django.conf.urls import url
from user.views import *

urlpatterns = [
    url(r'^login/?$', UserLogin.as_view()),
    url(r'^logout/?$', UserLogout.as_view()),
    url(r'^apply/list?$', ApplyList.as_view()),
#    url(r'^create/question?$', CreateQuestion.as_view()),
#    url(r'^create/section?$', CreateSection.as_view()),
#    url(r'^create/form?$', CreateForm.as_view()),
#    url(r'^modify/section?$', ModifySection.as_view()),
#    url(r'^modify/form?$', ModifyForm.as_view()),
    url(r'^create/apply?$', CreateApply.as_view()),
    url(r'^check/apply?$', CheckForm.as_view()),
#    url(r'^form/detail?$', CheckFormBase.as_view()),
#    url(r'^section/detail?$', CheckSectionBase.as_view()),
#    url(r'^question/detail?$', CheckQuestionBase.as_view()),
    url(r'^form/list?$', FormList.as_view()),
#    url(r'^section/list?$', SectionBaseList.as_view()),
#    url(r'^question/list?$', QuestionBaseList.as_view()),
    url(r'^finish/form?$', FinishForm.as_view()),
]