''' App URLS.py file. '''
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^mainpage$', views.mainpage),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
]
