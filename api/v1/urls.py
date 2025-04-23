from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from api.v1.views.orders import (
    OrderCreateView,
    OrderDeleteView,
    OrderListView,
    OrderUpdateView,
)

# Note: because the number of end points is not high, we are not seperating urls into seperate files, for the time being.
# We can seperate them into diffrent files like views
app_name = "api_v1"
urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),  # Login
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "orders/create", OrderCreateView.as_view(), name="order_create"
    ),  # Create Order
    path("orders/", OrderListView.as_view(), name="order_list"),
    path("orders/<int:pk>/update/", OrderUpdateView.as_view(), name="order_update"),
    path("orders/<int:pk>/delete/", OrderDeleteView.as_view(), name="order_delete"),
]
