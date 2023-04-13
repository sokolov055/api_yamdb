from rest_framework.routers import SimpleRouter
from django.urls import include, path

from .views import TitleViewSet, UsersViewSet, CategoryViewSet


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
    r'category',
    CategoryViewSet,
    basename='category'
)

urlpatterns = [
    path('v1/', include(router.urls)),
]
