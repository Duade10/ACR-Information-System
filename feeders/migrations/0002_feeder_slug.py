# Generated by Django 4.1b1 on 2022-07-16 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("feeders", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="feeder",
            name="slug",
            field=models.SlugField(blank=True, max_length=10, null=True, unique=True),
        ),
    ]
