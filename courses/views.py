import datetime

from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from courses.models import Course, Lesson, Subscription
from courses.paginators import CoursePaginator, LessonPaginator
from courses.serializers import (
    CourseDetailSerializer,
    CourseSerializer,
    LessonSerializer,
)
from courses.task import send_course_update_notification
from users.permissions import IsModers, IsOwner


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="description from swagger_auto_schema via method_decorator"
    ),
)
class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    pagination_class = CoursePaginator

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModers,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModers | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModers | IsOwner,)

        return super().get_permissions()

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()
        now = timezone.now()
        # Проверяем время последнего обновления
        if course.updated_at < now - datetime.timedelta(hours=4):
            send_course_update_notification.delay(course.id)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = (~IsModers, IsAuthenticated)

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated,)
    pagination_class = LessonPaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModers | IsOwner)


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModers | IsOwner)


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsOwner | ~IsModers)


class SubscriptionView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        course_id = request.data.get("course_id")
        course_item = get_object_or_404(Course, id=course_id)
        subs_item = Subscription.objects.filter(user=request.user, course=course_item)
        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=request.user, course=course_item)
            message = "Подписка добавлена"
        return Response({"message": message}, status=status.HTTP_200_OK)
