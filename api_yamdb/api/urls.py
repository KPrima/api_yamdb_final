from django.urls import include, path
from rest_framework import routers

from .views import (
    CategoryViewSet, CommentViewSet, GenreViewSet,
    ReviewViewSet, TitleViewSet, UserViewSet,
    get_token, user_registration
)

app_name = 'api'

router_v1 = routers.DefaultRouter()

router_v1.register(r'v1/users', UserViewSet, basename='users')
router_v1.register(r'v1/categories', CategoryViewSet)
router_v1.register(r'v1/genres', GenreViewSet)
router_v1.register(r'v1/titles', TitleViewSet)
router_v1.register(
    r'v1/titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)
router_v1.register(
    r'v1/titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review'
)

urlpatterns = [
    path('', include(router_v1.urls)),
    path('v1/auth/signup/', user_registration),
    path('v1/auth/token/', get_token),
]
