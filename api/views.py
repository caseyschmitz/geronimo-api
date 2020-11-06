from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .models import SpeedTest
from .serializers import SpeedTestSerializer

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'monitor': reverse('api:monitor-root', request=request, format=format)
    })

class SpeedTestList(generics.ListCreateAPIView):
    queryset = SpeedTest.objects.all()
    serializer_class = SpeedTestSerializer