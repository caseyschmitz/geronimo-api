from rest_framework import serializers
from django.contrib.auth.models import User
from .models import TestNode, SpeedTest

class TestNodeSerializer(serializers.HyperlinkedModelSerializer):
    speedtests = serializers.HyperlinkedRelatedField(many=True, view_name='speedtest-detail', read_only=True)
    class Meta:
        model = TestNode
        fields = ['url', 'id', 'name', 'uri', 'active', 'speedtests']

class SpeedTestSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    node = serializers.HyperlinkedRelatedField(many=False, view_name='testnode-detail', read_only=True)

    class Meta:
        model = SpeedTest
        fields = ['url', 'id', 'type', 'owner', 'node', 'created', 'modified', 'started', 'completed', 'data']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    speedtests = serializers.HyperlinkedRelatedField(many=True, view_name='speedtest-detail', read_only=True)
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'speedtests']
