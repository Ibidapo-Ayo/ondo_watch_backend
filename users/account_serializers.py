from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers

User = get_user_model()


class OfficialAccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=12,
        trim_whitespace=False,
    )

    role_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Group.objects.all(),
        source="groups",
        required=False,
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "role_ids",
            "is_active",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            "email": {"required": True},
            "is_active": {"required": False},
        }

    def create(self, validated_data):
        groups = validated_data.pop("groups", [])
        password = validated_data.pop("password")

        user = User.objects.create_user(
            password=password,
            **validated_data,
        )

        user.groups.set(groups)
        return user
