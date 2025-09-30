from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    Handles serialization and deserialization of User instances.
    """

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "date_joined",
            "last_login",
            "password",
        ]
        read_only_fields = ("id", "last_login", "date_joined")
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        """Create and return a new User instance using Django's create_user method."""
        password = validated_data.pop("password", None)
        is_staff = validated_data.pop("is_staff", False)
        user = User.objects.create_user(
            password=password, is_active=True, **validated_data
        )
        user.is_staff = is_staff
        user.save()
        return user

    def validate(self, data):
        """
        Validate the given data and raise a Validation error
        if there is already an admin user.
        """
        if data.get("is_staff"):
            if User.objects.filter(is_staff=True).exists():
                raise serializers.ValidationError(
                    {"is_staff": "Only one admin user is allowed."}
                )
        return data

    def update(self, instance, validated_data):
        """Update and return an existing User instance."""
        user_data = validated_data.copy()
        password = user_data.pop("password", None)

        if password is not None:
            instance.set_password(password)

        return super().update(instance, user_data)
