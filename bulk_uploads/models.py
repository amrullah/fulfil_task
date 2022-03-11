from django.contrib.postgres.indexes import HashIndex
from django.db import models


class CsvUploadTask(models.Model):
    UPLOADED = 'UP'
    PROCESSING = 'PR'
    FINISHED = 'FN'
    FAILED = 'FL'
    STATUS_CHOICES = [
        (UPLOADED, 'Uploaded'),
        (PROCESSING, 'Processing'),
        (FINISHED, 'Finished'),
        (FAILED, 'Failed')
    ]
    task_id = models.CharField(max_length=127, unique=True)
    total_rows = models.IntegerField(null=True)
    processed_rows = models.IntegerField(default=0)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default=UPLOADED)
    file = models.FileField()

    class Meta:
        indexes = [
            HashIndex(name='task_id_hash_idx', fields=['task_id'])
        ]

    def __str__(self):
        return f'Csv Upload: {self.task_id}'

    def change_status_to_processing(self):  # would have used django-fsm to enforce valid transitions
        self.status = self.PROCESSING
        self.save(update_fields=['status'])

    def change_status_to_finished(self):
        self.status = self.FINISHED
        self.save(update_fields=['status'])

    def change_status_to_failed(self):
        self.status = self.FAILED
        self.save(update_fields=['status'])

    def update_total_rows(self, number_of_rows: int):
        self.total_rows = number_of_rows
        self.save(update_fields=['total_rows'])

    def increment_processed_rows(self):
        self.refresh_from_db()  # would have thought of a more efficient way
        if self.processed_rows is None:
            self.processed_rows = 0
        self.processed_rows += 1
        self.save(update_fields=['processed_rows'])
