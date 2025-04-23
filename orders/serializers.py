from rest_framework import serializers

from orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=255,
        default="سفارش تستی",
    )
    count = serializers.IntegerField(
        default=1,
    )
    total_price = serializers.IntegerField(
        default=100,
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "name",
            "count",
            "total_price",
            "user",
            "created_at",
            "edited_at",
        ]
        read_only_fields = ["id", "created_at", "edited_at", "user"]
