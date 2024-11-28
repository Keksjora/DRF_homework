from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        user = User.objects.create(
            email="test@mail.ru", first_name="admin", last_name="admin"
        )

        user.set_password("12345678")

        user.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created admin user with email {user.email}!"
            )
        )
