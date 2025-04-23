from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Creates an admin and a normal user if they don't exist, and adds them to respective groups"

    def handle(self, *args, **kwargs):
        # Ensure the groups exist
        admin_group, created = Group.objects.get_or_create(name="admin")
        normal_user_group, created = Group.objects.get_or_create(name="normal_user")

        # Check if the admin user exists, if not, create it
        if not User.objects.filter(username="admin").exists():
            admin_user = User.objects.create_superuser(
                username="admin",
                password="admin123",  # noqa: S106
                email="admin@example.com",
            )
            admin_user.groups.add(admin_group)  # Add the admin user to the Admin group
            self.stdout.write(
                self.style.SUCCESS("Admin user created and added to 'admin' group")
            )
        else:
            admin_user = User.objects.get(username="admin")
            self.stdout.write(self.style.SUCCESS("Admin user already exists"))

        # Check if the normal user exists, if not, create it
        if not User.objects.filter(username="normaluser").exists():
            normal_user = User.objects.create_user(
                username="normaluser",
                password="normal123",  # noqa: S106
                email="user@example.com",
            )
            normal_user.groups.add(
                normal_user_group
            )  # Add the normal user to the 'Normal User' group
            self.stdout.write(
                self.style.SUCCESS(
                    "Normal user created and added to 'normal_user' group"
                )
            )
        else:
            normal_user = User.objects.get(username="normaluser")
            self.stdout.write(self.style.SUCCESS("Normal user already exists"))
