from django.conf.urls import url
from django.urls import path, include, re_path

from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),
    path('ws/chat/alarms/', views.alarm, name='alarm'),
]
