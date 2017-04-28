from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import detail_route

from mailgun.tasks import send_email, get_stats
from mailgun.serializers import EmailSerializer, EmailResultSerializer, StatsSerializer, StatsResultSerializer


class EmailHandle(APIView):
    def get(self, request, format=None):
        """
        Get an information about a mailing task
        ---
        response_serializer: EmailResultSerializer
        parameters:
            - name: id
              description: mailing task id
              paramType: query
              required: True
        """

        task_serializer = EmailResultSerializer(data=request.query_params)
        task_serializer.is_valid(raise_exception=True)
        task = send_email.AsyncResult(task_id=task_serializer.data['id'])
        return Response(EmailResultSerializer(instance=task).data)

    def post(self, request, format=None):
        """
        Send an email
        ---
        request_serializer: EmailSerializer
        response_serializer: EmailResultSerializer
        """
        serializer = EmailSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        task = send_email.delay(**serializer.data)
        task_serializer = EmailResultSerializer(task)
        return Response(data=task_serializer.data)


class StatsHandle(APIView):
    def get(self, request, format=None):
        """
        Get count of messages by task id.
        ---
        response_serializer: StatsResultSerializer
        parameters:
            - name: id
              description: task id that is received in the response of POST method 
              paramType: query
              required: True
        """
        task_serializer = StatsResultSerializer(data=request.query_params)
        task_serializer.is_valid(raise_exception=True)
        task = get_stats.AsyncResult(task_id=task_serializer.data['id'])
        return Response(StatsResultSerializer(instance=task).data)

    def post(self, request, format=None):
        """
        Create task to get statistics.
        ---
        request_serializer: StatsSerializer
        response_serializer: StatsResultSerializer
        """
        serializer = StatsSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        task = get_stats.delay(**serializer.data)
        task_serializer = StatsResultSerializer(task)
        return Response(data=task_serializer.data)
