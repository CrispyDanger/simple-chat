from rest_framework import serializers
from .models import Thread, Message
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
        ]


class MessageSerialzer(serializers.ModelSerializer):
    sender = UserSerializer()

    class Meta:
        model = Message
        fields = ["sender", "text", "is_read"]


class ThreadSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True)

    class Meta:
        model = Thread
        fields = [
            "id",
            "participants",
        ]
