from rest_framework.serializers import ModelSerializer

from users.models import CustomsUser, Payments


class PaymentsSerializer(ModelSerializer):
    class Meta:
        model = Payments
        fields = "__all__"


class CustomsUserDetailSerializer(ModelSerializer):
    payment_history = PaymentsSerializer(many=True, read_only=True)

    class Meta:
        model = CustomsUser
        fields = ["id", "email", "phone_number", "avatar", "city", "payment_history"]


class CustomsUserSerializer(ModelSerializer):
    class Meta:
        model = CustomsUser
        fields = "__all__"
