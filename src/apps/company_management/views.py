from rest_framework import viewsets, permissions, response, status

from .models import Company
from .serializers import CompanySerializer
from src.utils.custom_permissions import IsAdminOrReadOnly


class CompanyViewSet(viewsets.ModelViewSet):

    lookup_field = 'code'
    queryset = Company.objects.filter(is_active=True)
    serializer_class = CompanySerializer
    # permission_classes = (IsAdminOrReadOnly,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
