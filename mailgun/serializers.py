from rest_framework import serializers
from celery import states


class EmailSerializer(serializers.Serializer):
    email_from = serializers.EmailField(required=True)
    email_to = serializers.EmailField(required=True)
    subject = serializers.CharField(max_length=200, required=True)
    text = serializers.CharField(required=True)


states_list = [states.PENDING, states.SUCCESS, states.FAILURE]


class TaskSerializer(serializers.Serializer):
    id = serializers.CharField()
    state = serializers.CharField(required=False, help_text=','.join(states_list))
    result = serializers.JSONField(allow_null=True, required=False, help_text='dictionary object actually: id, message')
