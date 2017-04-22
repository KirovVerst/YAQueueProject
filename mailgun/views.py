from django.http import JsonResponse
from mailgun.tasks import send_simple_message


def email_handle(request):
    if request.method == "POST":
        data = {
            'email_from': request.POST['email_from'],
            'email_to': request.POST['email_to'],
            'text': request.POST['text'],
            'subject': request.POST['subject']
        }
        r = send_simple_message.delay(**data)
        return JsonResponse(data=dict(id=r.id))
    else:
        task_id = request.GET['task_id']
        task = send_simple_message.AsyncResult(task_id=task_id)
        data = dict(ready=task.ready())
        if data['ready']:
            data['res'] = task.get()
        return JsonResponse(data=data)
