from rest_framework import permissions
from rest_framework.generics import CreateAPIView

from orders.models import Order
from orders.serializers import OrderSerializer


class OrderCreateView(CreateAPIView):
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        # Automatically set the user to the currently authenticated user
        serializer.save(user=self.request.user)
