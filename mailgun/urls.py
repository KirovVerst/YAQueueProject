from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^sum_two/$', views.sum_two, name='sum'),
]
