from rest_framework.routers import SimpleRouter
from django.urls import include, path

from .views import TitleViewSet, UsersViewSet, CategoryViewSet, GenreViewSet


app_name = 'api'

router = SimpleRouter()

router.register(
    r'users',
    UsersViewSet,
    basename='users'
)

router.register(
    r'titles',
    TitleViewSet,
    basename='titles'
)


router.register(
    r'categories',
    CategoryViewSet,
    basename='categories'
)

router.register(
    r'genres',
    GenreViewSet,
    basename='genres'
)

urlpatterns = [
    path('v1/', include(router.urls)),
]
