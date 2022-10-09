# Generated by Django 4.1rc1 on 2022-07-23 19:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("stations_330", "0003_station_330_station_type"),
        ("troublereports", "0004_alter_troublereport_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="troublereport",
            name="station_or_line_station_132_330",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="trouble_reports_132_330",
                to="stations_330.station_330",
            ),
        ),
    ]
