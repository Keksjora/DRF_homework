from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from courses.models import Course
from users.models import CustomsUser, Payments
from users.serializers import (
    CustomsUserDetailSerializer,
    CustomsUserSerializer,
    PaymentsSerializer,
)
from users.services import (
    create_stripe_price,
    create_stripe_product,
    create_stripe_session,
)


class PaymentsViewSet(viewsets.ModelViewSet):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("payment_method", "paid_course", "paid_lesson")
    ordering_fields = ("payment_date",)

    def create(self, request, *args, **kwargs):
        """Создает новый платеж и взаимодействует с Stripe"""
        amount = request.data.get("amount")
        product_name = request.data.get("product_name")
        course_id = request.data.get("course_id")
        # Проверка на валидность входных данных
        if not product_name or amount is None:
            return Response(
                {"error": "Invalid input: product_name and amount are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Получение курса из базы данных
        if course_id:
            try:
                course = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                return Response(
                    {"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {"error": "Course ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            product = create_stripe_product(course)
            price = create_stripe_price(amount, product.id)
            session_id, session_url = create_stripe_session(price.id)
            payment = Payments.objects.create(
                user=request.user,
                payment_amount=amount,
                payment_method="Stripe",
                paid_course=course,  # Указываем оплаченный курс
            )
            # Возвращаем URL сессии
            return Response(
                {
                    "session_id": session_id,
                    "payment_id": payment.id,
                    "url": session_url,
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CustomsUserViewSet(viewsets.ModelViewSet):
    queryset = CustomsUser.objects.all()
    serializer_class = CustomsUserDetailSerializer


class CustomsUserCreateAPIView(CreateAPIView):
    serializer_class = CustomsUserSerializer
    queryset = CustomsUser.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if request.user.is_authenticated:
            request.user.last_login = timezone.now()
            request.user.save()
        return response
