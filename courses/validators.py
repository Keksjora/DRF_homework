import re

from rest_framework.serializers import ValidationError


class LinkVideoValidator:
    """Валидатор для модели урока, поля video_link"""

    message = "Ссылки доступны только с youtube.com"

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        youtube_link = (
            r"^(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[a-zA-Z0-9_-]+$"
        )
        tmp_field = dict(value).get(self.field)
        if not re.match(youtube_link, tmp_field):
            raise ValidationError(self.message)
