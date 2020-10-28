from rest_framework import viewsets, permissions

from .serializers import ProfileSerializer
from .models import Profile
from src.utils.custom_permissions import IsOwnerOrReadOnly

from django.contrib.auth import get_user


class ProfileViewSet(viewsets.ModelViewSet):

    lookup_field = 'code'
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
