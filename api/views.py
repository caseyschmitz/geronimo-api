from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from .models import SpeedTest, SpeedTestClient
from .serializers import SpeedTestClientSerializer, SpeedTestSerializer, UserSerializer
from .permissions import IsOwnerOrReadOnly


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'speedtest': reverse('speedtest-list', request=request, format=format),
        'speedtestclient': reverse('speedtestclient-list', request=request, format=format),
    })

class SpeedTestList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = SpeedTest.objects.all()
    serializer_class = SpeedTestSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SpeedTestDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = SpeedTest.objects.all()
    serializer_class = SpeedTestSerializer

class SpeedTestClientList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = SpeedTestClient.objects.all()
    serializer_class = SpeedTestClientSerializer

class SpeedTestClientDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = SpeedTestClient.objects.all()
    serializer_class = SpeedTestClientSerializer

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer