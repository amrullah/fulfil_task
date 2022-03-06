from django.contrib.postgres.indexes import HashIndex
from django.db import models


class CsvUploadTask(models.Model):
    STATUS_CHOICES = [
        ('UP', 'Uploaded'),
        ('PR', 'Processing'),
        ('FN', 'Finished'),
        ('FL', 'Failed')
    ]
    task_id = models.CharField(max_length=127, unique=True)
    total_rows = models.IntegerField(null=True)
    processed_rows = models.IntegerField(null=True)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='UP')
    file = models.FileField()

    class Meta:
        indexes = [
            HashIndex(name='task_id_hash_idx', fields=['task_id'])
        ]

    def __str__(self):
        return f'Csv Upload: {self.task_id}'
