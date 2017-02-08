from django.conf.urls import url

from . import views

mainView=views.CaseViews()

urlpatterns = [
        url(r'^$', mainView.viewCase),
]

