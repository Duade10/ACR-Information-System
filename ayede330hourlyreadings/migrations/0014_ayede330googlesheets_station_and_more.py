# Generated by Django 4.1rc1 on 2022-08-28 12:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("stations_330", "0006_station_330_active_load_flow_and_more"),
        ("ayede330hourlyreadings", "0013_alter_ayede330googlesheets_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="ayede330googlesheets",
            name="station",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="station_google_sheets",
                to="stations_330.station_330",
            ),
        ),
        migrations.AddField(
            model_name="ayede330googlesheets",
            name="station_name",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
