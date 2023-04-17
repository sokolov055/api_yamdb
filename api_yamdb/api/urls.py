from rest_framework.routers import SimpleRouter
from django.urls import include, path

from .views import (TitleViewSet, UsersViewSet,
                    SignUpView, AuthToken)


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

auth_patterns = [
    path('signup/', SignUpView.as_view()),
    path('token/', AuthToken.as_view())
]

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/', include(auth_patterns))
]
