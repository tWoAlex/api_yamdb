from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, registration, send_jwt_token

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('v1/auth/signup/', registration),
    path('v1/auth/token/', send_jwt_token),
    path('v1/', include(router.urls)),
]
