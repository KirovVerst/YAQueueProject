from __future__ import absolute_import, unicode_literals
from celery import shared_task
from qproject import settings
import requests

from multiprocessing import Manager

manag = Manager()
serviceLock = manag.Lock()
state = manag.dict()


@shared_task
def send_email(email_from, email_to, text, subject):
    r = requests.post(
        settings.MAILGUN_API_BASE_URL + '/messages',
        auth=("api", settings.MAILGUN_API_KEY),
        data={"from": "Excited User <{}>".format(email_from),
              "to": [email_to],
              "subject": subject,
              "text": text})
    try:
        if email_from in state:
            state[email_from] += 1
        else:
            state[email_from] = 1
        response = r.json()
        response['count'] = state[email_from]
        return response
    except:
        print(r.content)
        return dict(result=r.content)


@shared_task
def get_stats(email):
    return dict(email=email, count=state[email])
