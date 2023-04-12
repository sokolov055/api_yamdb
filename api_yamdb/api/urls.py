from rest_framework.routers import SimpleRouter
from django.urls import include, path

from .views import TitleViewSet, UsersViewSet


app_name = 'api'

router = SimpleRouter()

router.register(
    'users',
    UsersViewSet,
    basename='users'
)

router.register(
    'titles',
    TitleViewSet,
    basename='titles'
)

urlpatterns = [
    path('v1/', include(router.urls)),
]
