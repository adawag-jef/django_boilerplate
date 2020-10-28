from django.urls import path, include
from rest_framework import routers
from .views import CompanyViewSet


router = routers.DefaultRouter()
router.register(r'company-management', CompanyViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
