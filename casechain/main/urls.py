from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from . import views

mainView=views.CaseViews()

urlpatterns = [
        url(r'^$', mainView.viewCases),
        url(r'^([0-9]+)/$', mainView.viewCase),
        url(r'^add$', mainView.getCaseForm),
        url(r'^create$',mainView.addCase),
        url(r'^import$',csrf_exempt(mainView.receiveCase)),
]

