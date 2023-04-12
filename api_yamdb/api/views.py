from reviews.models import Title, User
from .serializers import TitleReadSerializer, UsersSerializer
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
