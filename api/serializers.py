from rest_framework_json_api import serializers
from django.contrib.auth.models import User
from .models import SpeedTestClient, SpeedTestServer, SpeedTestResult, SpeedTest

class SpeedTestClientSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = SpeedTestClient
        fields = ['url', 'id', 'name', 'uri', 'active', 'owner']

class SpeedTestServerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SpeedTestServer
        fields = ['url', 'host', 'server_id', 'name', 'sponsor', 'country', 'country_code', 'distance_km', 'latitude', 'longitude']

class SpeedTestResultSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SpeedTestResult
        fields = ['url', 'timestamp', 'server', 'ping', 'bytes_received', 'bytes_sent', 'download_bytes', 'upload_bytes', 'image_url']


class SpeedTestSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    client = serializers.HyperlinkedRelatedField(many=False, view_name='speedtestclient-detail', read_only=True)

    class Meta:
        model = SpeedTest
        fields = ['url', 'id', 'type', 'owner', 'client', 'created', 'modified', 'started', 'completed', 'result']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    speedtests = serializers.HyperlinkedRelatedField(many=True, view_name='speedtest-detail', read_only=True)
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'password', 'speedtests']
