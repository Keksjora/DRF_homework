from rest_framework.routers import SimpleRouter

from users.apps import UsersConfig
from users.views import CustomsUserViewSet, PaymentsViewSet

router = SimpleRouter()


router.register(r"payments", PaymentsViewSet, basename="payments")
router.register(r"users", CustomsUserViewSet, basename="users")
app_name = UsersConfig.name

urlpatterns = []

urlpatterns += router.urls
