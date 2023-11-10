from rest_framework import serializers
from .models import *

class StationAPISerializer(serializers.ModelSerializer):
    RENT_NO = serializers.IntegerField(source='station_id')
    STA_LOC = serializers.CharField(source='location')
    RENT_NM = serializers.CharField(source='station_name')
    STA_LAT = serializers.DecimalField(max_digits=11, decimal_places=8, source='latitude')
    STA_LONG = serializers.DecimalField(max_digits=11, decimal_places=8, source='longitude')
    STA_ADD1 = serializers.CharField(source='addr1')
    STA_ADD2 = serializers.CharField(source='addr2', allow_blank=True)

    class Meta:
        model = Station
        fields = ['RENT_NO', 'STA_LOC', 'RENT_NM', 'STA_LAT', 'STA_LONG', 'STA_ADD1', 'STA_ADD2']

class UsageAPISerializer(serializers.Serializer):
    RENT_NM = serializers.CharField(source='use_date')
    STATION_NO = serializers.IntegerField()
    GENDER_CD = serializers.CharField(source='gender', allow_blank=True)
    AGE_TYPE = serializers.CharField(source='age_range')
    USE_CNT = serializers.IntegerField(source='use_count')

    def create(self, validated_data):
        station = Station.objects.get(station_id=validated_data['STATION_NO'])
        usage = Usage.objects.create(
            station_id = station.id,
            use_count = validated_data['use_count'],
            use_date = validated_data['use_date'],
            gender = validated_data['gender'],
            age_range = validated_data['age_range'],
        )
        usage.save()
        return usage
    
    class Meta:
        model = Usage
        fields = ['RENT_NM', 'STATION_NO', 'GENDER_CD', 'AGE_TYPE', 'USE_CNT']

class UsageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Usage
        fields = '__all__'

class StationSerializer(serializers.ModelSerializer):
    usages = UsageSerializer(many=True)

    class Meta:
        model = Station
        fields = '__all__'