# Generated by Django 4.1rc1 on 2022-07-23 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("notifications", "0008_alter_notification_to_station_132_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="notification",
            name="url",
            field=models.URLField(blank=True, null=True),
        ),
    ]
