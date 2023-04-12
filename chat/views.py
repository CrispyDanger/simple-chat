from .serializers import (
    ThreadSerializer,
    MessageReadSerializer,
    MessageWriteSerializer,
    UnreadMessageSerializer,
)
from rest_framework.response import Response
from rest_framework.generics import (
    ListCreateAPIView,
    DestroyAPIView,
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView,
)
from .models import Thread, Message
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.views import APIView


class ThreadListView(ListCreateAPIView):
    serializer_class = ThreadSerializer

    def get_queryset(self):
        threads = Thread.objects.filter(participants=self.request.user)
        return threads

    def get_users(self, request):
        participant = User.objects.get(username=request.data["username"])
        return request.user, participant

    def post(self, request):
        try:
            # Try to retrieve the current user and the participant from the request data
            currentUser, participant = self.get_users(request)
            # Try to get the thread that contains both the participant and the current user
            participantThreads = Thread.objects.filter(participants=participant)
            userThreads = participantThreads.get(participants=currentUser)
        except User.DoesNotExist:
            # If the participant doesn't exist, return a 404 Not Found response
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Thread.MultipleObjectsReturned:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Thread.DoesNotExist:
            # If the thread doesn't exist, create a new one and add the participants
            newThread = Thread.objects.create()
            newThread.add_participant(currentUser)
            newThread.add_participant(participant)
            serializer = ThreadSerializer(newThread)
            # Return a response indicating that the new thread was created
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # If the thread exists, serialize it and return the response
            serializer = ThreadSerializer(userThreads)
            return Response(serializer.data, status=status.HTTP_200_OK)


class ThreadDestroyView(DestroyAPIView):
    serializer_class = ThreadSerializer
    lookup_url_kwarg = "id"

    def get_object(self):
        return Thread.objects.get(id=self.kwargs.get("id"))


class ThreadMessageListView(ListAPIView):
    serializer_class = MessageReadSerializer
    lookup_url_kwarg = "id"

    def get_queryset(self):
        return Message.objects.filter(thread=self.kwargs.get("id"))


class ThreadMessageCreateView(CreateAPIView):
    serializer_class = MessageWriteSerializer
    lookup_url_kwarg = "thread_id"

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs["context"] = self.get_serializer_context()

        # Check for "id" in url
        if "thread_id" in self.kwargs:
            modified_data = self.request.data.copy()
            modified_data["thread"] = self.kwargs.get("thread_id")
            kwargs["data"] = modified_data
            return serializer_class(*args, **kwargs)

        # Else, move on.
        return serializer_class(*args, **kwargs)


class ThreadMessageDetailview(RetrieveUpdateAPIView):
    serializer_class = MessageReadSerializer

    def get_object(self):
        thread_id = self.kwargs.get("thread_id")
        message_id = self.kwargs.get("message_id")
        return Message.objects.get(thread=thread_id, id=message_id)

    def update(self, *args, **kwargs):
        message = Message.objects.get(
            id=self.kwargs.get("message_id"),
            thread=self.kwargs.get("thread_id"),
            is_read=False,
        )
        if message.sender != self.request.user:
            message.is_read = True
            message.save()
        return Response(status=status.HTTP_200_OK)


class UnreadMessageView(APIView):
    def get(self, request):
        messages = Message.objects.filter(sender=request.user, is_read=False)
        serializer = UnreadMessageSerializer(messages)
        return Response(serializer.data, status=status.HTTP_200_OK)
