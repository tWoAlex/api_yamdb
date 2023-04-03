from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .v1 import views as v1_views


v1_router = DefaultRouter()
v1_router.register('users', v1_views.UserViewSet)
v1_router.register('categories',
                   v1_views.CategoryViewSet, basename='categories')
v1_router.register('genres',
                   v1_views.GenreViewSet, basename='genres')
v1_router.register('titles', v1_views.TitleViewSet, basename='titles')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews',
                   v1_views.ReviewViewSet, basename='reviews')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    v1_views.CommentViewSet, basename='comments')

api_v1_urls = [
    path('', include(v1_router.urls)),
    path('auth/signup/', v1_views.registration),
    path('auth/token/', v1_views.send_jwt_token),
]

urlpatterns = [
    path('v1/', include(api_v1_urls)),
]
