# Generated by Django 4.2.2 on 2025-01-18 23:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Contents", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="text",
            field=models.TextField(verbose_name="متن نظر"),
        ),
    ]
