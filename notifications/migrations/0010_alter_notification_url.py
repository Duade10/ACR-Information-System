# Generated by Django 4.1rc1 on 2022-07-23 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("notifications", "0009_notification_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="notification",
            name="url",
            field=models.CharField(blank=True, max_length=132, null=True),
        ),
    ]
