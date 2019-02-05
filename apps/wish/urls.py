from django.conf.urls import url,include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$',  views.index),
    url(r'register/$',  views.register),
    url(r'login/$',  views.login),
    url(r'wishes/$',views.wishes),
    url(r'wishes/new/$',views.new),
    url(r'wishes/create/$',views.create),
    url(r'logout/$',views.logout),
    url(r'wishes/(?P<id>\d+)/edit/$',views.edit),
    url(r'wishes/update/(?P<id>\d+)/$',views.update),
    url(r'wishes/(?P<id>\d+)/remove/$',views.remove),
    url(r'wishes/(?P<id>\d+)/granted/$',views.granted),
    url(r'stats/$',views.stats),
    url(r'wishes/(?P<id>\d+)/like/$', views.like),
]
