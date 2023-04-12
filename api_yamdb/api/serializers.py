from rest_framework import serializers
from reviews.models import Title, User


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')


class TitleReadSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Title
