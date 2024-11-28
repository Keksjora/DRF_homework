from django.db import models


class Course(models.Model):
    """Модель курс"""

    title = models.CharField(max_length=150, verbose_name="название")
    picture = models.ImageField(
        upload_to="images/", verbose_name="превью(картинка)", blank=True, null=True
    )
    description = models.TextField(max_length=350, verbose_name="название")
    owner = models.ForeignKey(
        "users.CustomsUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="владелец",
        help_text="укажите владельца",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"
        ordering = ["title"]


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name="название")
    description = models.TextField(max_length=500, verbose_name="название")
    picture = models.ImageField(
        upload_to="images/", verbose_name="превью(картинка)", blank=True, null=True
    )
    video_link = models.URLField(blank=True, null=True)
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    owner = models.ForeignKey(
        "users.CustomsUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="владелец",
        help_text="укажите владельца",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
        ordering = ["title"]


class Subscription(models.Model):
    """Модель подписки на обновление курса"""

    user = models.ForeignKey("users.CustomsUser", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "course")
