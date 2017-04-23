from django.conf.urls import url
from mailgun.views import EmailHandle

urlpatterns = [
    url(r'^email/$', EmailHandle.as_view())
]
