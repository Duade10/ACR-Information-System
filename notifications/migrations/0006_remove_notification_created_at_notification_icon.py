# Generated by Django 4.1rc1 on 2022-07-23 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("notifications", "0005_alter_notification_to_station_132_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="notification",
            name="created_at",
        ),
        migrations.AddField(
            model_name="notification",
            name="icon",
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
