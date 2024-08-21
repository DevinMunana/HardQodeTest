from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
import io
from rest_framework.parsers import JSONParser

from product.api.v1.permissions import IsStudentOrIsAdmin, ReadOnlyOrIsAdmin
from product.courses.serializers import (CourseSerializer,
                                                  CreateCourseSerializer,
                                                  CreateGroupSerializer,
                                                  CreateLessonSerializer,
                                                  GroupSerializer,
                                                  LessonSerializer)
from product.users.serializers import SubscriptionSerializer
from product.courses.models import Course
from product.users.models import Subscription, Balance


class LessonViewSet(viewsets.ModelViewSet):
    """Уроки."""

    permission_classes = (IsStudentOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return LessonSerializer
        return CreateLessonSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.lessons.all()


class GroupViewSet(viewsets.ModelViewSet):
    """Группы."""

    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GroupSerializer
        return CreateGroupSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.groups.all()


class CourseViewSet(viewsets.ModelViewSet):
    """Курсы """

    initial_queryset = Course.objects.all()

    def already_aquired_courses(self):
        from product.users.models import CustomUser
        user = CustomUser.objects.get(id=self.request.user.id)
        aquired_courses = user.courses.all()
        return aquired_courses

    for course in already_aquired_courses():
        initial_queryset.remove(course)

    queryset = initial_queryset
    serializer_class = CourseSerializer
    permission_classes = (ReadOnlyOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CourseSerializer
        return CreateCourseSerializer

    @action(
        methods=['post'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def pay(self, request, pk):
        """Покупка доступа к курсу (подписка на курс)."""

        course = Course.objects.get(id=pk)
        balance = Balance.objects.get(user=request.user)
        if balance.balance >= course.price:
            stream = io.BytesIO(request.data)
            data = JSONParser().parse(stream)
            serializer = SubscriptionSerializer(data=data)
            if serializer.is_valid:
                serializer.save()
                subscription = Subscription.objects.get(user_name=request.user.username)
                subscription.user = request.user
                subscription.course = course
                subscription.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return HttpResponse("I need more money!")