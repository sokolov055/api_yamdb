from reviews.models import Title, User, Category, Genre
from .serializers import (TitleReadSerializer,
                          UsersSerializer,
                          CategorySerializer,
                          GenreSerializer,
                          TitleWriteSerializer)
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    lookup_field = 'username'


class TitleViewSet(ModelViewSet):
    """
    Получить список всех объектов. Права доступа: Доступно без токена
    """
    queryset = Title.objects.all()
    serializer_class = TitleReadSerializer

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
