from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from tours.models import *
from accounts.serializers.user_serializers import *


class TransactionSerializer(serializers.ModelSerializer):
    sender = serializers.CharField()

    class Meta:
        model = Transaction
        fields = '__all__'


class DiscountCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = '__all__'


class TourSerializer(serializers.ModelSerializer):
    owner = SpecialUserSerializer(read_only=True)
    class Meta:
        model = Tour
        fields = ['title', 'cost', 'capacity',
                  'start_date', 'end_date', 'id', 'owner','bookers','image']
        read_only_fields = ['id','owner','bookers']

    def create(self, validated_data):
        validated_data['owner_id'] = self.context.get("owner")
        return super().create(validated_data)