from rest_framework import serializers
from .models import Profile
from src.utils.common_serializers import (
    BaseCodeSerializer)


class ProfileSerializer(serializers.ModelSerializer,
                        BaseCodeSerializer,
                        ):

    user = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['code', 'bio', 'location',
                  'birth_date', 'user', 'company', 'created_at']

    def get_user(self, obj):
        return {
            'username': obj.user.username,
            'code': obj.user.code
        }

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.company:
            ret['company'] = {'code': instance.company.code,
                              'name': instance.company.name}
        return ret
