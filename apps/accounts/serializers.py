from django.contrib.auth.models import User
from rest_framework import serializers

class SignUpSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style = {'input_type': 'password'}, write_only = True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password":"Password fields didn't match"})
        return attrs

    def create(self, validated_data):
        validated_data.pop["password2"]
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )

        return user