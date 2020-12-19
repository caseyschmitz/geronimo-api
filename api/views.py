from rest_framework import generics, permissions, authentication, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework_json_api.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from .models import SpeedTest, SpeedTestClient
from .serializers import SpeedTestClientSerializer, SpeedTestSerializer, UserSerializer
from .permissions import IsOwnerOrReadOnly, IsOwner, IsSelf


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'speed-tests': reverse('speedtest-list', request=request, format=format),
        'speed-test-clients': reverse('speedtestclient-list', request=request, format=format),
        'users': reverse('user-list', request=request, format=format),
    })

# adapted from https://www.django-rest-framework.org/api-guide/authentication/
class APIAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'is_superuser': user.is_superuser
        })

class SpeedTestList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = SpeedTest.objects.all()
    serializer_class = SpeedTestSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SpeedTestDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = SpeedTest.objects.all()
    serializer_class = SpeedTestSerializer

class SpeedTestClientList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = SpeedTestClient.objects.all()
    serializer_class = SpeedTestClientSerializer

    def get(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            # Admin can list all Speed Test Clients
            self.permission_classes = [permissions.IsAdminUser]
            self.queryset = SpeedTestClient.objects.all()
        else:
            # Authenticated users can list all Speed Test Clients that they own
            self.permission_classes = [permissions.IsAuthenticated, IsOwner]
            self.queryset = SpeedTestClient.objects.filter(owner=self.request.user)
        return super(SpeedTestClientList, self).get(request, *args, **kwargs)

    #def get_queryset(self):
    #    return SpeedTestClient.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SpeedTestClientDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = SpeedTestClient.objects.all()
    serializer_class = SpeedTestClientSerializer

class UserList(generics.ListCreateAPIView):
    #authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Only Admin can list Users
    def get(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            self.permission_classes = [permissions.IsAdminUser]
            self.queryset = User.objects.all()
        return super(UserList, self).get(request, *args, **kwargs)

    # Anyone can add a User
    def post(self, request, *args, **kwargs):
        self.permission_classes = [permissions.AllowAny]
        return super(UserList, self).post(request, *args, **kwargs)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            # Admin can get any user
            self.permission_classes = [permissions.IsAdminUser]
            self.queryset = User.objects.all()
        else:
            # Authenticated users can get themselves
            self.permission_classes = [IsSelf]
            self.queryset = User.objects.filter(username=self.request.user)
        return super(UserDetail, self).get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            # Admin can update any user
            self.permission_classes = [permissions.IsAdminUser]
            self.queryset = User.objects.all()
        else:
            # Authenticated users can update themselves
            self.permission_classes = [IsSelf]
            self.queryset = User.objects.filter(username=self.request.user)
        return super(UserDetail, self).put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            # Admin can update any user
            self.permission_classes = [permissions.IsAdminUser]
            self.queryset = User.objects.all()
        else:
            # Authenticated users can update themselves
            self.permission_classes = [IsSelf]
            self.queryset = User.objects.filter(username=self.request.user)
        return super(UserDetail, self).patch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            # Admin can delete any user
            self.permission_classes = [permissions.IsAdminUser]
            self.queryset = User.objects.all()
        else:
            # Authenticated users can delete themselves
            self.permission_classes = [IsSelf]
            self.queryset = User.objects.filter(username=self.request.user)
        return super(UserDetail, self).delete(request, *args, **kwargs)

class UserCreate(generics.CreateAPIView):
    resource_name = 'users'
    model = User
    parser_classes = [JSONParser]
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
