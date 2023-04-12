from rest_framework import serializers
from .models import Thread, Message
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
        ]


class MessageReadSerializer(serializers.ModelSerializer):
    sender = UserSerializer()

    class Meta:
        model = Message
        fields = ["sender", "text", "is_read", "id"]


class MessageWriteSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Message
        fields = ["sender", "text", "is_read", "thread"]


class ThreadSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True)

    class Meta:
        model = Thread
        fields = [
            "id",
            "participants",
        ]
        read_only_fields = ["id"]


class UnreadMessageSerializer(serializers.ModelSerializer):
    unread_messages = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ["unread_messages"]

    def get_unread_messages(self, obj):
        return obj.count()
