from django.urls import include, path
from rest_framework.routers import SimpleRouter

from courses.apps import CoursesConfig
from courses.views import (
    CourseViewSet,
    LessonCreateAPIView,
    LessonDestroyAPIView,
    LessonListAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
    SubscriptionView,
)

router = SimpleRouter()
router.register(r"course", CourseViewSet, basename="course")

app_name = CoursesConfig.name

urlpatterns = [
    path("", include(router.urls)),
    path("lesson/create", LessonCreateAPIView.as_view(), name="lesson_create"),
    path("lesson/", LessonListAPIView.as_view(), name="lesson_list"),
    path("lesson/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson_detail"),
    path(
        "lesson/update/<int:pk>/", LessonUpdateAPIView.as_view(), name="lesson_update"
    ),
    path(
        "lesson/delete/<int:pk>/", LessonDestroyAPIView.as_view(), name="lesson_delete"
    ),
    path("subscription/", SubscriptionView.as_view(), name="subscription"),
]

urlpatterns += router.urls
