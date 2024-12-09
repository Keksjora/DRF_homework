from rest_framework.test import APITestCase

from users.models import Course, CustomsUser, Payments
from users.services import (
    create_stripe_price,
    create_stripe_product,
    create_stripe_session,
)


class PaymentsTests(APITestCase):
    def setUp(self):
        self.user = CustomsUser.objects.create(
            email="testuser@example.com", is_active=True
        )
        self.user.set_password("testpassword")
        self.user.save()
        self.course = Course.objects.create(
            title="Test Course", description="Test description", owner=self.user
        )

    def test_create_product(self):
        """Тестирование создания продукта в Stripe"""
        product = create_stripe_product(
            self.course
        )  # Используйте объект курса, а не строку
        self.assertIn("id", product)  # Проверяем, что продукт был создан и имеет ID

    def test_create_price(self):
        """Тестирование создания цены в Stripe"""
        product = create_stripe_product(
            self.course
        )  # Используйте объект курса, а не строку
        price = create_stripe_price(1000, product.id)
        self.assertIn("id", price)  # Проверяем, что цена была создана
