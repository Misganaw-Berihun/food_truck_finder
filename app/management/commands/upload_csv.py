import csv
from django.core.management.base import BaseCommand
from app.models import CSVData


class Command(BaseCommand):
    help = 'Upload CSV data'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file_path',
            type=str,
            help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file_path']
        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:

                CSVData.objects.create(data=row)
        self.stdout.write(
            self.style.SUCCESS('CSV file uploaded successfully.')
        )
