# Generated by Django 5.1.3 on 2024-11-21 11:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0002_alter_course_picture_alter_lesson_picture_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                help_text="укажите владельца",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="владелец",
            ),
        ),
        migrations.AddField(
            model_name="lesson",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                help_text="укажите владельца",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="владелец",
            ),
        ),
    ]