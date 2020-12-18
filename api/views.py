from rest_framework import generics, permissions, authentication, status
from rest_framework_json_api.parsers import JSONParser
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
        'speed-tests': reverse('speedtest-list', request=request, format=format),
        'speed-test-clients': reverse('speedtestclient-list', request=request, format=format),
        'users': reverse('user-list', request=request, format=format),
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

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SpeedTestClientDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = SpeedTestClient.objects.all()
    serializer_class = SpeedTestClientSerializer

class UserList(generics.ListAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserCreate(generics.CreateAPIView):
    resource_name = 'users'
    model = User
    parser_classes = [JSONParser]
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
