from src.utils.Utils import Utility
from src.utils.common_serializers import BaseCodeSerializer
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str, smart_bytes
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer, BaseCodeSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'code']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.ModelSerializer):

    code = serializers.CharField(read_only=True)
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(
        max_length=255, min_length=3, read_only=True)
    tokens = serializers.JSONField(read_only=True)

    class Meta:
        model = User
        fields = ['code', 'email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account is disabled contact admin.')

        return {
            'code': user.code,
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens()
        }
        # return super().validate(attrs)


class LogoutSerializer(serializers.Serializer):

    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs.get('refresh')
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']

    def reset_password(self, request):
        data = request.data
        email = data.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)

            current_site = get_current_site(request=request).domain
            relativeLink = reverse(
                'password_reset_confirm',
                kwargs={'uidb64': uidb64, 'token': token})

            absurl = 'http://' + current_site + relativeLink
            email_body = 'Hello, \nUse link below to reset your password \n' + absurl
            data = {
                'email_body': email_body,
                'to_email': user.email,
                'email_subject': 'Reset your Password'
            }
            Utility.send_email(data)


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)

    token = serializers.CharField(
        min_length=1, write_only=True)

    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The Reset link is invalid', 401)

            user.set_password(password)
            return user.save()
        except Exception:
            raise AuthenticationFailed('The Reset link is invalid', 401)


class UserSerializer(serializers.ModelSerializer):

    code = serializers.CharField(read_only=True)

    class Meta:
        fields = ['code', 'email', 'username', 'is_active']
        model = User

    # def create(self, obj):
    #     obj.is_active = False
    #     return obj.save()
