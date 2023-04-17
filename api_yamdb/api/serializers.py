from rest_framework import serializers
from reviews.models import Category, Genre, Review, Title, User


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
        lookup_field = 'username'

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


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        lookup_field = 'slug'
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre
        lookup_field = 'slug'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        required=False,
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Review
        fields = ('id', 'score', 'text', 'pub_date', 'author',)
        read_only_fields = ('id', 'pub_date', 'author',)

    def validate(self, data):
        is_review_exist = Review.objects.filter(
            author=self.context['request'].user,
            title=self.context['view'].kwargs['title_id']
        ).exists()

        if self.context['request'].method == 'POST' and is_review_exist:
            raise serializers.ValidationError(
                'Вы не можете оставить такой же отзыв дважды.')

        return data
