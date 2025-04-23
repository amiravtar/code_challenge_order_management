from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from orders.models import Order


class Command(BaseCommand):
    help = "Import default groups and assign permissions."

    def handle(self, *args, **kwargs):
        # Get the content type for the Order model
        order_content_type = ContentType.objects.get_for_model(model=Order)

        # Fetch all permissions for the Order model
        permissions = Permission.objects.filter(content_type=order_content_type)

        # Create or get the default admin group
        admin_group, created = Group.objects.get_or_create(name="admin")

        # Add all permissions for the Order model to the admin group
        admin_group.permissions.set(permissions)

        # Output to the console
        if created:
            self.stdout.write(
                self.style.SUCCESS("Admin group created and permissions added.")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS("Admin group already exists. Permissions updated.")
            )
        # Create or get the default normal user group
        normal_group, created = Group.objects.get_or_create(name="normal_user")

        if created:
            self.stdout.write(self.style.SUCCESS("Normal user group created."))
        else:
            self.stdout.write(self.style.SUCCESS("Normal user group already exists."))
