from django_filters import rest_framework as filters
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated

from orders.filters import OrderFilter
from orders.models import Order
from orders.permissions import IsOrderOwnerOrAdmin
from orders.serializers import OrderSerializer


class OrderCreateView(CreateAPIView):
    # the defualt permission class is is_authenticated, so we dont overide it
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        # Automatically set the user to the currently authenticated user
        serializer.save(user=self.request.user)


class OrderListView(ListAPIView):
    serializer_class = OrderSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = OrderFilter

    def get_queryset(self):  # type: ignore
        # checking for owner or admin permission
        # user exist becuse of is_authenticated defualt permission
        user = self.request.user
        if user.has_perm("orders.view_all_orders"):  # type: ignore
            return Order.objects.all()
        return Order.objects.filter(user=user)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "price",
                openapi.IN_QUERY,
                description="قیمت",
                type=openapi.TYPE_NUMBER,
            ),
            openapi.Parameter(
                "min_price",
                openapi.IN_QUERY,
                description="حداقل قیمت",
                type=openapi.TYPE_NUMBER,
            ),
            openapi.Parameter(
                "max_price",
                openapi.IN_QUERY,
                description="حداکثر قیمت",
                type=openapi.TYPE_NUMBER,
            ),
            openapi.Parameter(
                "date_after",
                openapi.IN_QUERY,
                description="از تاریخ",
                type=openapi.TYPE_STRING,
                format="date",
            ),
            openapi.Parameter(
                "date_before",
                openapi.IN_QUERY,
                description="تا تاریخ",
                type=openapi.TYPE_STRING,
                format="date",
            ),
        ]
    )
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


class OrderDeleteView(DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOrderOwnerOrAdmin]


class OrderUpdateView(UpdateAPIView):
    """
    Edit an existing order.
    Only the order owner or users with 'edit_all_orders' permission can edit.
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOrderOwnerOrAdmin]
