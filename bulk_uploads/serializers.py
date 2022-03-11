from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from .models import CsvUploadTask


class CsvUploadTaskSerializer(ModelSerializer):
    status = CharField(source='get_status_display')

    class Meta:
        model = CsvUploadTask
        fields = ['task_id', 'status', 'processed_rows', 'total_rows', 'file']