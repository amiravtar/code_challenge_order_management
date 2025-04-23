from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from api.v1.views.orders import OrderCreateView

# Note: because the number of end points is not high, we are not seperating urls into seperate files, for the time being.
# We can seperate them into diffrent files like views
app_name = "api_v1"
urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),  # Login
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "orders/create", OrderCreateView.as_view(), name="order_create"
    ),  # Create Order
]
