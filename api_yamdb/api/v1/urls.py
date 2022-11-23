from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    RegistrationAPIView, ReviewViewSet, TitleViewSet,
                    TokenAPIView, UserViewSet)

v1_router = DefaultRouter()
v1_router.register(r'users', UserViewSet, basename='users')
v1_router.register(r'titles', TitleViewSet, basename='title')
v1_router.register(r'categories', CategoryViewSet, basename='categories')
v1_router.register(r'genres', GenreViewSet, basename='genres')

v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
auth_patterns = [
    path('signup/', RegistrationAPIView.as_view(), name='signup'),
    path('token/', TokenAPIView.as_view(), name='token')
]
urlpatterns = [
    path('', include(v1_router.urls)),
    path('auth/', include(auth_patterns)),
]
