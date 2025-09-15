from rest_framework import serializers
from .models import User

class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id",
                  "username",
                  "first_name",
                  "last_name",
                  "email",
                  "is_staff",
                  "last_login",
                  "is_active",
                  "date_joined"]
        read_only_fields = ('id', "last_login", "date_joined")
        required_fields = ( "first_name", "last_name", "username", "email", "password")

    def create(self, validated_data):
        password = validated_data.get('password')
        is_staff = validated_data.get('is_staff')
        instance = self.Meta.model(**validated_data)
        if password:
            instance.set_password(password)
        if is_staff and is_staff == "true":
            instance.is_staff = True
        user = User.objects.create_user(**validated_data)
        return user