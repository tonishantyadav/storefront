# Generated by Django 4.2.2 on 2023-06-23 05:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0002_remove_product_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="slug",
            field=models.SlugField(default="-"),
            preserve_default=False,
        ),
    ]
