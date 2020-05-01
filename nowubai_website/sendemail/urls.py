from django.conf.urls import url

from sendemail import views

urlpatterns = [
    url("^/sendemail",views.sendemail)
]