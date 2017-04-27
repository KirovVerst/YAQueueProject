from __future__ import absolute_import, unicode_literals
from celery import shared_task
from qproject import settings
import requests


@shared_task
def send_simple_message(email_from, email_to, text, subject):
    r = requests.post(
        settings.MAILGUN_API_BASE_URL + '/messages',
        auth=("api", settings.MAILGUN_API_KEY),
        data={"from": "Excited User <{}>".format(email_from),
              "to": [email_to],
              "subject": subject,
              "text": text})
    try:
        return r.json()
    except:
        print(r.content)
        return dict(result=r.content)
