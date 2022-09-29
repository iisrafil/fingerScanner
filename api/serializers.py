from rest_framework import serializers

from api.models import Intruder, Data, Finger


class FingerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finger
        fields = ['device', 'image']


class IntruderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intruder
        fields = ['device', 'finger', 'image']


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = ['device', 'finger', 'match_result', 'match_time', 'match_percent', 'transport_time',
                  'transport_medium', 'photo', 'photo_time']