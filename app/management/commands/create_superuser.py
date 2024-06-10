from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os


class Command(BaseCommand):
    """
    Django management command to create a superuser if one does
    not already exist.

    Attributes:
        help (str): A brief description of what the command does.

    Methods:
        handle(*args, **options):
            Executes the command logic to check for the existence of
            the superuser and create one if necessary.
    """
    help = 'Create a superuser if not exists'

    def handle(self, *args, **options):
        """
        Executes the command to create a superuser if one does not
        already exist.

        """
        User = get_user_model()
        if not User.objects.filter(
                username=os.getenv('DJANGO_SUPERUSER_USERNAME')
             ).exists():
            User.objects.create_superuser(
                username=os.getenv('DJANGO_SUPERUSER_USERNAME'),
                email=os.getenv('DJANGO_SUPERUSER_EMAIL'),
                password=os.getenv('DJANGO_SUPERUSER_PASSWORD')
            )
            self.stdout.write(self.style.SUCCESS(
                'Superuser created successfully.')
                )
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists.'))
