from django.db import models


class CSVData(models.Model):
    data = models.JSONField()

    def __str__(self):
        return str(self.id)
