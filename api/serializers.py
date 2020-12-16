from rest_framework_json_api import serializers
from django.contrib.auth.models import User
from .models import SpeedTestClient, SpeedTest

class SpeedTestClientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SpeedTestClient
        fields = ['url', 'id', 'name', 'uri', 'active']

class SpeedTestSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    node = serializers.HyperlinkedRelatedField(many=False, view_name='speedtestclient-detail', read_only=True)

    class Meta:
        model = SpeedTest
        fields = ['url', 'id', 'type', 'owner', 'node', 'created', 'modified', 'started', 'completed', 'data']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    speedtests = serializers.HyperlinkedRelatedField(many=True, view_name='speedtest-detail', read_only=True)
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'speedtests']
