# Generated by Django 4.1.1 on 2022-10-05 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ayede330hourlyreadings", "0020_ayede330googlesheetrange_station"),
    ]

    operations = [
        migrations.AddField(
            model_name="ayede330hourlyreading",
            name="acc_stations_load",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="ayede330hourlyreading",
            name="active_load_flow",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="ayede330hourlyreading",
            name="transformer_hourly_load",
            field=models.BooleanField(default=True),
        ),
    ]
