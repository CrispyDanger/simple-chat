from .serializers import ThreadSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Thread, Message
from rest_framework import status
from django.contrib.auth.models import User


class ThreadView(APIView):
    def get_users(self, request):
        participant = User.objects.get(username=request.data["username"])
        return request.user, participant

    def get(self, request):
        # Retrieve all threads that the current user is a participant of
        threads = Thread.objects.filter(participants=request.user)
        # Serialize the threads and return the response
        serializer = ThreadSerializer(threads, many=True)
        return Response(serializer.data)

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

    def delete(self, request):
        # Retrieve the current user and the participant from the request data
        try:
            currentUser, participant = self.get_users(request)
            participantThreads = Thread.objects.filter(participants=participant)
            participantThreads.get(participants=currentUser).delete()
            # Return a 204 No Content response to indicate that the thread was successfully deleted
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Thread.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
