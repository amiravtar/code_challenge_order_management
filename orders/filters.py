from django_filters import rest_framework as filters

from .models import Order


class OrderFilter(filters.FilterSet):
    price = filters.NumberFilter(field_name="total_price")
    min_price = filters.NumberFilter(field_name="total_price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="total_price", lookup_expr="lte")
    date = filters.DateFromToRangeFilter(field_name="created_at")

    class Meta:
        model = Order
        fields = ["min_price", "max_price", "date"]
