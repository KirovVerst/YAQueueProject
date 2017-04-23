from rest_framework import serializers


class EmailSerializer(serializers.Serializer):
    email_from = serializers.EmailField(required=True)
    email_to = serializers.EmailField(required=True)
    subject = serializers.CharField(max_length=200, required=True)
    text = serializers.CharField(required=True)


class TaskSerializer(serializers.Serializer):
    id = serializers.CharField()
    state = serializers.CharField(required=False)
    result = serializers.JSONField(allow_null=True, required=False)

