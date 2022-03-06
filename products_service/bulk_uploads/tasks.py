import csv

from celery import shared_task
from django.conf import settings

from products.services.ProductCreator import ProductCreator
from .models import CsvUploadTask


def __update_the_total_rows_count_of_task(upload_task):
    with open(settings.MEDIA_DIR / upload_task.file.name, 'r') as file:
        reader = csv.DictReader(file)
        number_of_rows_in_csv = 0
        for _ in reader:
            number_of_rows_in_csv += 1
        upload_task.update_total_rows(number_of_rows_in_csv)


@shared_task
def process_csv_file(task_id: str):
    print(f"Now in Celery Task: {task_id}")
    # TODO: this task id should be in 'uploaded' state
    # TODO: handle exception
    upload_task: CsvUploadTask = CsvUploadTask.objects.get(task_id=task_id)
    upload_task.change_status_to_processing()

    try:
        __update_the_total_rows_count_of_task(upload_task)

        with open(settings.MEDIA_DIR / upload_task.file.name, 'r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                name, sku, description = row['name'], row['sku'], row['description']
                # TODO: do bulk insert query for efficiency
                product = ProductCreator.create(name, sku, description)
                print(f'** Created Product: {product}')
                upload_task.increment_processed_rows()

            upload_task.change_status_to_finished()
    except:
        upload_task.change_status_to_failed()
        # TODO: need a field to store the traceback
