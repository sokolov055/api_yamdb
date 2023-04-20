from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .mixins import ModelMixinSet
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title, User
from api.filters import TitleFilter
from .permissions import (IsAdminPermission, IsAdminOrReadOnly,
                          IsAuthorAdminModerOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ObtainTokenSerializer,
                          ReviewSerializer, SignUpSerializer,
                          TitleReadSerializer, TitleWriteSerializer,
                          UsersSerializer, NotAdminSerializer)
from api_yamdb.settings import NOREPLY_YAMDB_EMAIL


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAdminPermission,)
    lookup_field = "username"
    filter_backends = (SearchFilter, )
    search_fields = ('username', )

    @action(
        methods=["GET", "PATCH"],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request):
        serializer = UsersSerializer(request.user)
        if request.method == "PATCH":
            if request.user.is_admin:
                serializer = UsersSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            else:
                serializer = NotAdminSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)


@api_view(['POST'])
def sign_up(request):
    serializer = SignUpSerializer(data=request.data)
    email = request.data.get('email')
    serializer.is_valid(raise_exception=True)
    try:
        user, created = User.objects.get_or_create(**serializer.validated_data)
    except IntegrityError:
        return Response('Попробуйте другой email или username',
                        status=status.HTTP_400_BAD_REQUEST)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Регистрация',
        message=confirmation_code,
        from_email=NOREPLY_YAMDB_EMAIL,
        recipient_list=[email],
        fail_silently=False
    )
    return Response(serializer.data,
                    status=status.HTTP_200_OK)


class AuthToken(APIView):
    def post(self, request):
        serializer = ObtainTokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data['username']
            confirmation_code = serializer.data['confirmation_code']
            user = get_object_or_404(User, username=username)
            if confirmation_code != user.confirmation_code:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            token = RefreshToken.for_user(user)
            return Response(
                {'token': str(token.access_token)},
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)


class TitleViewSet(ModelViewSet):
    """
    Получить список всех объектов. Права доступа: Доступно без токена
    """
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class CategoryViewSet(ModelMixinSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'


class GenreViewSet(ModelMixinSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminOrReadOnly,
                          IsAuthorAdminModerOrReadOnly)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_queryset(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminOrReadOnly,
                          IsAuthorAdminModerOrReadOnly)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        review = get_object_or_404(Review.objects.filter(title_id=title.id),
                                   pk=review.id)
        return review.comments.all()

    def perform_queryset(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        review = get_object_or_404(Review.objects.filter(title_id=title.id),
                                   pk=review.id)
        serializer.save(author=self.request.user, review=review)
