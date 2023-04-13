from reviews.models import Title, User, Category
from .serializers import (TitleReadSerializer,
                          UsersSerializer,
                          CategorySerializer)
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer


class TitleViewSet(ModelViewSet):
    """
    Получить список всех объектов. Права доступа: Доступно без токена
    """
    queryset = Title.objects.all()
    serializer_class = TitleReadSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
