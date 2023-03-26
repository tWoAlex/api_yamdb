from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (UserViewSet, registration, send_jwt_token,
                    CategoryViewSet, GenreViewSet, TitleViewSet,
                    ReviewViewSet, CommentViewSet)
# from .views import TitleList, TitleDetail

v1_router = DefaultRouter()
v1_router.register(r'users', UserViewSet)
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('titles', TitleViewSet, basename='titles')
# v1_router.register('titles', TitleList, basename='titles')
v1_router.register(
    r'titles(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', registration),
    path('v1/auth/token/', send_jwt_token),
]
