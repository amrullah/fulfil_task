import traceback
from pathlib import Path

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile

from .. import logger
from ..models import CsvUploadTask
from .task_id_generator import TaskIdGenerator
from ..tasks import process_csv_file


class UploadedFileHandler:
    @staticmethod
    def save_file_and_trigger_processing(uploaded_file: InMemoryUploadedFile) -> str:
        new_task_id = UploadedFileHandler.__get_new_task_id()

        file_path = f"csv/products_{new_task_id}.csv"
        UploadedFileHandler.__ensure_directory_exists(file_path)
        UploadedFileHandler.__write_file_to_disk_and_trigger_processing(new_task_id, file_path, uploaded_file)

        return new_task_id

    @staticmethod
    def __write_file_to_disk_and_trigger_processing(task_id, file_path, uploaded_file):
        try:
            UploadedFileHandler.__write_file_to_disk(file_path, uploaded_file)
        except:
            upload_task = CsvUploadTask.objects.create(task_id=task_id, file=file_path, status=CsvUploadTask.FAILED)
            logger.info(f"{upload_task} could not be saved to disk: {traceback.format_exc()}")
            return
        upload_task = CsvUploadTask.objects.create(task_id=task_id, file=file_path)
        logger.info(f"{upload_task} is now Uploaded")

        process_csv_file.delay(task_id)

    @staticmethod
    def __get_new_task_id() -> str:
        while True:
            task_id = TaskIdGenerator.generate_new_task_id()
            task_id_already_exists = CsvUploadTask.objects.filter(task_id=task_id).exists()
            if not task_id_already_exists:
                break

        return task_id

    @staticmethod
    def __ensure_directory_exists(file_path):
        file_path = file_path.split("/")[0]
        Path(settings.MEDIA_DIR / file_path).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def __write_file_to_disk(file_path, uploaded_file):
        with open(str(settings.MEDIA_DIR / file_path), 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
                logger.info("Wrote chunk to file")