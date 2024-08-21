from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)
from rest_framework.routers import DefaultRouter

from product.courses.views import CourseViewSet, GroupViewSet, LessonViewSet
from product.users.views import UserViewSet

v1_router = DefaultRouter()
v1_router.register('users', UserViewSet, basename='users')
v1_router.register('courses', CourseViewSet, basename='courses')
v1_router.register(
    r'courses/(?P<course_id>\d+)/lessons', LessonViewSet, basename='lessons'
)
v1_router.register(
    r'courses/(?P<course_id>\d+)/groups', GroupViewSet, basename='groups'
)

urlpatterns = [
    path("", include(v1_router.urls)),
    path(r"^auth/", include('djoser.urls')),
    path(r"^auth/", include('djoser.urls.authtoken')),
    # Создание нового пользователя api/v1/auth/users/
    # Авторизация пользователя     api/v1/auth/token/login/
]

urlpatterns += [
    path(
        'schema/',
        SpectacularAPIView.as_view(api_version='api/v1'),
        name='schema'
    ),
    path(
        'swagger/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),
    path(
        'redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc',
    ),
]