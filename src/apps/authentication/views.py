from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.utils.encoding import (smart_str, DjangoUnicodeDecodeError)
from django.utils.http import urlsafe_base64_decode

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    LogoutSerializer,
    ResetPasswordEmailRequestSerializer,
    SetNewPasswordSerializer,
    UserSerializer,
)

from src.utils.custom_permissions import IsOwnerOrReadOnly

User = get_user_model()


class RegisterView(generics.CreateAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        return Response(user_data, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):

    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):

    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class RequestPasswordResetEmail(generics.GenericAPIView):

    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.reset_password(request)

        return Response({'success':
                         'We have sent you a link to reset your password'},
                        status=status.HTTP_200_OK)


class PasswordTokenCheckAPIView(generics.GenericAPIView):

    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error':
                                 'Token is not valid, please request a new one'},
                                status=status.HTTP_401_UNAUTHORIZED)

            return Response({'success': True,
                             'message': 'Credentials Valid',
                             'uidb64': uidb64,
                             'token': token},
                            status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError:
            return Response({'error':
                             'Token is not valid, please request a new one'},
                            status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({'success': True,
                         'message': 'Password Reset Success'},
                        status=status.HTTP_200_OK)


class ArchiveUserView(generics.RetrieveDestroyAPIView):

    lookup_field = 'code'
    queryset = User.objects.all()
    permission_classes = (
        permissions.IsAdminUser,
    )

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        user = instance.save()
        user = UserSerializer(user).data
        return Response(user, status=status.HTTP_200_OK)
