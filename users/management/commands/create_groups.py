from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Создает группы в базе данных"

    def handle(self, *args, **kwargs):
        group_names = ["moders"]

        for name in group_names:
            group, created = Group.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Группа "{name}" была создана.'))
            else:
                self.stdout.write(
                    self.style.WARNING(f'Группа "{name}" уже существует.')
                )
