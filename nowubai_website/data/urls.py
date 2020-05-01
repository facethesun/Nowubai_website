from django.conf.urls import url

from data import views

urlpatterns = [
    url("^/index",views.index)
]