from django.db import models


class Course(models.Model):
    """Модель курс"""

    title = models.CharField(max_length=150, verbose_name="название")
    picture = models.ImageField(upload_to="images/", verbose_name="превью(картинка)")
    description = models.TextField(max_length=350, verbose_name="название")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"
        ordering = ["title"]


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name="название")
    description = models.TextField(max_length=500, verbose_name="название")
    picture = models.ImageField(upload_to="images/", verbose_name="превью(картинка)")
    video_link = models.URLField()
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
        ordering = ["title"]
