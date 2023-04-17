from rest_framework import serializers
from reviews.models import Title, User


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        if data.get('username') != 'me':
            return data
        raise serializers.ValidationError(
            'Не подходящее имя пользователя'
        )


class ObtainTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=15)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')

        def validate(self, data):
            if data.get('username') != 'me':
                return data
            raise serializers.ValidationError(
                'Не подходящее имя пользователя'
            )


class TitleReadSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Title
