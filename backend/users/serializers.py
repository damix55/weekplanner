from rest_framework import serializers
from users.models import User
import django.contrib.auth.password_validation as validators
from django.utils.translation import gettext as _

class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'user_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, password):
        if len(password) < 6:
            raise serializers.ValidationError(
                _("Password must be longer than 6 characters.")
            )
        return password

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance