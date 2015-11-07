from rest_framework import serializers
from services.models import *

class TrackingSerializer(serializers.ModelSerializer):
    lat = serializers.FloatField()
    long = serializers.FloatField()

    class Meta:
        model = Tracking

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "starttime": instance.starttime,
            "stoptime": instance.stoptime
        }

class PathSerializer(serializers.ModelSerializer):
    class Meta:
        model = Path

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Path
