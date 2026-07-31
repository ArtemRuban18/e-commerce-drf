from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    password2 = serializers.CharField(write_only = True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Password fileds didn't match"})

        validate_password(attrs['password'])
        return attrs

    def validate_email(self, value):
        if User.objects.filter(email = value).exists():
            raise serializers.ValidationError("User with this email elready exists")

    def create(self, validated_data):
        validated_data.pop('password2')

        user = User.objects.create_user(
            **validated_data
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only = True)
    