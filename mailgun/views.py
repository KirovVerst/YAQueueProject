from django.http import JsonResponse
from mailgun.tasks import add


def sum_two(request):
    if request.method == 'POST':
        r = add.delay(int(request.POST.get('a', '0')),
                      int(request.POST.get('b', '0')))
        data = dict(id=r.id)
    else:
        task_id = request.GET['task_id']
        task = add.AsyncResult(task_id=task_id)
        data = dict(ready=task.ready())
        if data['ready']:
            data['res'] = task.get()
    return JsonResponse(data=data)
