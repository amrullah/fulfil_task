from django.db import models

# Create your models here.


class Product(models.Model):
    sku = models.CharField(primary_key=True, max_length=127)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    description = models.TextField()

    def __str__(self):
        return f'sku: {self.sku} | {self.name}'

