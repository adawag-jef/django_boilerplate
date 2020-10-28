from rest_framework import serializers
from .models import Company
from src.utils.common_serializers import BaseCodeSerializer


class CompanySerializer(serializers.ModelSerializer, BaseCodeSerializer):

    is_active = serializers.BooleanField(default=True, read_only=True)

    class Meta:
        fields = ['code', 'name', 'is_active', 'created_at']
        model = Company

    def create(self, validated_data):
        company = super().create(validated_data)
        return Company.objects.get(id=company.id)
