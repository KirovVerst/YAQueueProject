from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^email/$', views.email_handle)
]
