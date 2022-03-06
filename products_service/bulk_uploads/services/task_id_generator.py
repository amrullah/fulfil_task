import random
import string


class TaskIdGenerator:
    @staticmethod
    def generate_new_task_id():
        length = 10
        return ''.join(random.sample(
            string.ascii_letters + string.digits, length
        ))
