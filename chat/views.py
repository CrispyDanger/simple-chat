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
from django.contrib.auth import get_user_model
from rest_framework.views import APIView


class ThreadListView(ListCreateAPIView):
    """
    A view that gets a list of threads.

    Attributes:
    serializer_class (ThreadSerializer): The serializer used to deserialize and serialize Thread instances.
    User (get_user_model()): Gets current user instance
    """

    serializer_class = ThreadSerializer
    User = get_user_model()

    def get_queryset(self):
        threads = Thread.objects.filter(participants=self.request.user)
        return threads

    def get_users(self, request):
        participant = self.User.objects.get(username=request.data["username"])
        return request.user, participant

    def post(self, request):
        try:
            # Try to retrieve the current user and the participant from the request data
            currentUser, participant = self.get_users(request)
            # Try to get the thread that contains both the participant and the current user
            participantThreads = Thread.objects.filter(participants=participant)
            userThreads = participantThreads.get(participants=currentUser)
        except self.User.DoesNotExist:
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
    """
    A view that deletes a Thread object.

    Attributes:
    serializer_class (ThreadSerializer): The serializer used to deserialize and serialize Thread instances.
    lookup_url_kwarg (str): The URL keyword argument to use when retrieving the thread to delete.
    """

    serializer_class = ThreadSerializer
    lookup_url_kwarg = "id"

    def get_object(self):
        """
        Retrieves the Thread instance to be deleted.

        Returns:
        Thread: The Thread instance with the given id.
        """
        return Thread.objects.get(id=self.kwargs.get("id"))


class ThreadMessageListView(ListAPIView):
    """
    A view that returns a list of messages for a Thread.

    Attributes:
    serializer_class (MessageReadSerializer): The serializer used to serialize the Message instances.
    lookup_url_kwarg (str): The URL keyword argument to use when retrieving the thread messages.
    """

    serializer_class = MessageReadSerializer
    lookup_url_kwarg = "id"

    def get_queryset(self):
        """
        Retrieves the list of messages for the Thread.

        Returns:
        QuerySet: A QuerySet containing the messages for the Thread.
        """
        return Message.objects.filter(thread=self.kwargs.get("id"))


class ThreadMessageCreateView(CreateAPIView):
    """
    A view that creates a new Message object for a Thread.

    Attributes:
    serializer_class (MessageWriteSerializer): The serializer used to deserialize and serialize Message instances.
    lookup_url_kwarg (str): The URL keyword argument to use when retrieving the Thread id.
    """

    serializer_class = MessageWriteSerializer
    lookup_url_kwarg = "thread_id"

    def get_serializer(self, *args, **kwargs):
        """
        Returns the serializer instance that will be used to deserialize and serialize Message instances.

        Returns:
        MessageWriteSerializer: The serializer instance that will be used to deserialize and serialize Message instances.
        """
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
    """
    A view that retrieves and updates a Message object for a Thread.

    Attributes:
    serializer_class (MessageReadSerializer): The serializer used to serialize the Message instance.
    """

    serializer_class = MessageReadSerializer

    def get_object(self):
        """
        Retrieves the Message instance to retrieve or update.

        Returns:
        Message: The Message instance with the given thread and message ids.
        """
        thread_id = self.kwargs.get("thread_id")
        message_id = self.kwargs.get("message_id")
        return Message.objects.get(thread=thread_id, id=message_id)

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to retrieve a Message instance.

        If the Message instance was sent by another user, sets the is_read attribute to True.

        Returns:
        Response: The serialized Message instance.
        """
        response = super().get(request, *args, **kwargs)
        messages = self.get_object()
        if messages.sender != self.request.user:
            messages.is_read = True
            messages.save()
        return response


class UnreadMessageView(APIView):
    """
    A view that returns a list of unread messages for the current user.

    """

    def get(self, request, format=None):
        messages = Message.objects.filter(is_read=False).exclude(sender=request.user)
        serializer = UnreadMessageSerializer(messages)
        return Response(serializer.data, status=status.HTTP_200_OK)
