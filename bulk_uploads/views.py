import json
import traceback

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet

from . import logger
from .models import CsvUploadTask
from .serializers import CsvUploadTaskSerializer
from .services.file_upload_handler import UploadedFileHandler


class CsvUploadTaskViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = CsvUploadTask.objects.all()
    serializer_class = CsvUploadTaskSerializer
    lookup_field = 'task_id'


@csrf_exempt
def file_upload_view(request):
    if not request.method == 'POST':
        return HttpResponse(status=405, content_type="application/json")
    try:
        uploaded_file = request.FILES['file']
    except Exception as e:
        logger.error(f"Could not find the file: {traceback.format_exc()}")
        return HttpResponse(json.dumps({"error": "File not Found. Contact Amrullah for help."}),
                            content_type="application/json", status=500)

    try:
        csv_task_id = UploadedFileHandler.save_file_and_trigger_processing(uploaded_file)
    except Exception as e:
        logger.error(f"Error in saving the file: {traceback.format_exc()}")
        raise

    return HttpResponse(json.dumps({"task_id": csv_task_id}),
                        content_type="application/json", status=202)

