from rest_framework.permissions import BasePermission

from orders.models import Order


class IsOrderOwnerOrAdmin(BasePermission):
    """
    Custom permission to only allow owners of an order to update/delete it,
    unless the user has edit_all or delete_all permission.
    """

    def has_object_permission(self, request, view, obj: Order) -> bool:  # type: ignore
        user = request.user
        if request.method in ["PUT", "PATCH"]:
            return obj.user == user or user.has_perm("orders.edit_all_orders")
        if request.method == "DELETE":
            return obj.user == user or user.has_perm("orders.delete_all_orders")
        return False
