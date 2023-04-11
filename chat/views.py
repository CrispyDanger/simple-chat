from .serializers import ThreadSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .models import Thread, Message


class ThreadView(ListAPIView):
    def get(self, request):
        threads = Thread.objects.filter(participants=request.user)
        serializer = ThreadSerializer(threads, many=True)
        return Response(serializer.data)
