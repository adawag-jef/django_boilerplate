from rest_framework import serializers


class BaseCodeSerializer(serializers.Serializer):
    code = serializers.SerializerMethodField(read_only=True)

    def get_code(self, obj):
        code = self.Meta.model.objects.get(id=obj.id).code
        return code
