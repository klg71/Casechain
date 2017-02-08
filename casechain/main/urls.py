from django.conf.urls import url

from . import views

mainView=views.CaseViews()

urlpatterns = [
        url(r'^$', mainView.viewCase),
        url(r'^hash/$', mainView.addCase),
]

