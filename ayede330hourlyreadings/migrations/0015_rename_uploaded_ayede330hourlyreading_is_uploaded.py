# Generated by Django 4.1 on 2022-08-29 17:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ayede330hourlyreadings", "0014_ayede330googlesheets_station_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="ayede330hourlyreading",
            old_name="uploaded",
            new_name="is_uploaded",
        ),
    ]
