# Generated by Django 4.1rc1 on 2022-07-22 17:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("stations_132", "0004_station_132_station_type"),
        ("stations_330", "0003_station_330_station_type"),
        ("notifications", "0003_remove_notification_notification_type_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="notification",
            name="from_station",
        ),
        migrations.RemoveField(
            model_name="notification",
            name="to_station",
        ),
        migrations.AddField(
            model_name="notification",
            name="from_station_132",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="notifications_from",
                to="stations_132.station_132",
            ),
        ),
        migrations.AddField(
            model_name="notification",
            name="from_station_330",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="notifications_from",
                to="stations_330.station_330",
            ),
        ),
        migrations.AddField(
            model_name="notification",
            name="to_station_132",
            field=models.ManyToManyField(
                null=True,
                related_name="notifications_to",
                to="stations_132.station_132",
            ),
        ),
        migrations.AddField(
            model_name="notification",
            name="to_station_330",
            field=models.ManyToManyField(
                null=True,
                related_name="notifications_to",
                to="stations_330.station_330",
            ),
        ),
    ]
