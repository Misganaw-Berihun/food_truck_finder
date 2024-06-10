# admin.py
from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from .models import CSVData
from .forms import CSVUploadForm
import csv

class CSVDataAdmin(admin.ModelAdmin):
    change_list_template = "admin/csv_data_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload-csv/', self.upload_csv),
        ]
        return custom_urls + urls

    def upload_csv(self, request):
        if request.method == "POST":
            form = CSVUploadForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = request.FILES['csv_file']
                reader = csv.DictReader(csv_file.read().decode('utf-8').splitlines())
                for row in reader:
                    CSVData.objects.create(data=row)
                self.message_user(request, "CSV file uploaded successfully.")
                return redirect("..")
        else:
            form = CSVUploadForm()
        return render(request, "admin/upload_csv.html", {"form": form})

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['upload_csv_url'] = 'upload-csv/'
        return super().changelist_view(request, extra_context=extra_context)


admin.site.register(CSVData, CSVDataAdmin)
