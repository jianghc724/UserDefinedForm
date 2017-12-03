from django.conf.urls import url
from user.views import *

urlpatterns = [
    url(r'^login/?$', UserLogin.as_view()),
    url(r'^logout/?$', UserLogout.as_view()),
    url(r'^apply/list?$', ApplyList.as_view()),
    url(r'^create/apply?$', CreateApply.as_view()),
    url(r'^form/list?$', FormList.as_view()),
    url(r'^cbd/?$', CBDForm.as_view()),
    url(r'^cex/?$', CEXForm.as_view()),
    url(r'^dops/?$', DOPSForm.as_view()),
    url(r'^oot/?$', OOTForm.as_view()),
    url(r'^pat/?$', PATForm.as_view()),
    url(r'^create/cbd/?$', CreateCBD.as_view()),
    url(r'^create/cex/?$', CreateCEX.as_view()),
    url(r'^create/dops/?$', CreateDOPS.as_view()),
    url(r'^create/oot/?$', CreateOOT.as_view()),
    url(r'^create/pat/?$', CreatePAT.as_view()),
    url(r'^create/user/?$', CreateUser.as_view()),
]