from django.contrib.postgres.indexes import GinIndex, HashIndex, BTreeIndex
from django.contrib.postgres.search import SearchVectorField, SearchVector
from django.db import models

# Create your models here.


class Product(models.Model):
    sku = models.CharField(primary_key=True, max_length=127)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    description = models.TextField()
    # description_vector = SearchVectorField(null=True)  # used for full text search over description

    class Meta:
        indexes = [
            GinIndex(SearchVector('description', config='english'), name='description_search_vector_idx'),
            HashIndex(name='sku_hash_idx', fields=['sku'], include=['name', 'is_active', 'description']),
            BTreeIndex(name='name_btree_idx', fields=['name'], include=['sku', 'is_active', 'description'])
        ]

    def __str__(self):
        return f'sku: {self.sku} | {self.name}'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.sku = self.sku.lower()
        super().save(force_insert, force_update, using, update_fields)