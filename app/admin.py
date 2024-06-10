from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from .models import CSVData
from .forms import CSVUploadForm
import csv


class CSVDataAdmin(admin.ModelAdmin):
    """
    Admin interface for the CSVData model, providing custom
    functionality to upload CSV files.

    Attributes:
        change_list_template (str): Path to the custom change
        list template.

    Methods:
        get_urls():
            Extends the default admin URLs with a custom URL for
            uploading CSV files.
        upload_csv(request):
            Handles the CSV upload functionality, processing the
            uploaded file and creating CSVData objects.
        changelist_view(request, extra_context=None):
            Adds custom context data to the change list view, including
            the URL for CSV upload.
    """
    change_list_template = "admin/csv_data_changelist.html"

    def get_urls(self):
        """
        Extends the default admin URLs with a custom URL for uploading
        CSV files.

        Returns:
            list: The combined list of default and custom URLs.
        """
        urls = super().get_urls()
        custom_urls = [
            path('upload-csv/', self.upload_csv),
        ]
        return custom_urls + urls

    def upload_csv(self, request):
        """
        Handles the CSV upload functionality, processing the uploaded
        file and creating CSVData objects.

        Args:
            request (HttpRequest): The request object containing POST
            data and uploaded files.

        Returns:
            HttpResponse: The response object, redirecting to the change
            list view upon successful upload.
        """
        if request.method == "POST":
            form = CSVUploadForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = request.FILES['csv_file']
                reader = csv.DictReader(
                    csv_file.read().decode('utf-8').splitlines())
                for row in reader:
                    CSVData.objects.create(data=row)
                self.message_user(request, "CSV file uploaded successfully.")
                return redirect("..")
        else:
            form = CSVUploadForm()
        return render(request, "admin/upload_csv.html", {"form": form})

    def changelist_view(self, request, extra_context=None):
        """
        Adds custom context data to the change list view, including the
        URL for CSV upload.

        Args:
            request (HttpRequest): The request object containing the user's
            request data. extra_context (dict, optional): Additional context
            data to pass to the template.

        Returns:
            HttpResponse: The response object rendering the change list view
            with the extra context.
        """
        extra_context = extra_context or {}
        extra_context['upload_csv_url'] = 'upload-csv/'
        return super().changelist_view(request, extra_context=extra_context)


admin.site.register(CSVData, CSVDataAdmin)
