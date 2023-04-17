from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (CategoryViewSet, GenreViewSet, ReviewViewSet, TitleViewSet,
                    UsersViewSet, SignUpView, AuthToken)


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

router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews_list'
)

auth_patterns = [
    path('signup/', SignUpView.as_view()),
    path('token/', AuthToken.as_view())
]

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/', include(auth_patterns))
]
