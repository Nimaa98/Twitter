# Generated by Django 4.2.2 on 2025-01-11 20:17

import Core.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="image",
            name="Image",
            field=models.ImageField(
                upload_to=Core.models.upload_to, verbose_name="Image"
            ),
        ),
    ]
