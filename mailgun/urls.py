from django.conf.urls import url
from mailgun.views import EmailHandle, StatsHandle

urlpatterns = [
    url(r'^email/$', EmailHandle.as_view()),
    url(r'^stats/$', StatsHandle.as_view())
]
