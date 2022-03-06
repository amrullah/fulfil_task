from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile

from ..models import CsvUploadTask
from .task_id_generator import TaskIdGenerator
from ..tasks import process_csv_file


class UploadedFileHandler:
    @staticmethod
    def save_file_and_trigger_processing(uploaded_file: InMemoryUploadedFile) -> str:
        new_task_id = UploadedFileHandler.__get_new_task_id()

        file_path = f"csv/products_{new_task_id}.csv"
        with open(str(settings.MEDIA_DIR / file_path), 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        CsvUploadTask.objects.create(task_id=new_task_id, file=file_path)
        process_csv_file.delay(new_task_id)
        # process_csv_file(new_task_id)

        return new_task_id

    @staticmethod
    def __get_new_task_id() -> str:
        while True:
            task_id = TaskIdGenerator.generate_new_task_id()
            task_id_already_exists = CsvUploadTask.objects.filter(task_id=task_id).exists()
            if not task_id_already_exists:
                break

        return task_id
