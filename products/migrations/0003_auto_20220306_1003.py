# Generated by Django 3.2 on 2022-03-06 10:03

import django.contrib.postgres.indexes
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_description_search_vector_idx'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='product',
            index=django.contrib.postgres.indexes.HashIndex(fields=['sku'], include=('name', 'is_active', 'description'), name='sku_hash_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=django.contrib.postgres.indexes.BTreeIndex(fields=['name'], include=('sku', 'is_active', 'description'), name='name_btree_idx'),
        ),
    ]