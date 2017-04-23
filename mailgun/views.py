from rest_framework.views import APIView
from rest_framework.response import Response

from mailgun.tasks import send_simple_message
from mailgun.serializers import EmailSerializer, TaskSerializer


class EmailHandle(APIView):
    def get(self, request, format=None):
        """
        Get an information about a mailing task
        ---
        response_serializer: TaskSerializer
        parameters:
            - name: id
              description: mailing task id
              paramType: query
              required: True
        """

        task_serializer = TaskSerializer(data=request.query_params)
        task_serializer.is_valid(raise_exception=True)
        task = send_simple_message.AsyncResult(task_id=task_serializer.data['id'])
        return Response(TaskSerializer(instance=task).data)

    def post(self, request, format=None):
        """
        Send an email
        ---
        request_serializer: EmailSerializer
        response_serializer: TaskSerializer
        """
        serializer = EmailSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        task = send_simple_message.delay(**serializer.data)
        task_serializer = TaskSerializer(task)
        return Response(data=task_serializer.data)