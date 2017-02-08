from django.conf.urls import url

from . import views

mainView=views.CaseViews()

urlpatterns = [
        url(r'^$', mainView.viewCases),
        url(r'^([0-9]+)/$', mainView.viewCase),
        url(r'^add$', mainView.getCaseForm),
]

