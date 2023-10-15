from rest_framework import serializers


class OrderNotFoundResponseSchema(serializers.Serializer):
    status = serializers.CharField(max_length=20, required=True)
    description = serializers.CharField(max_length=250, required=True)
