from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from courses.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    number_of_lessons = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_number_of_lessons(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "picture",
            "description",
            "number_of_lessons",
            "lessons",
        ]
