# Generated by Django 4.1rc1 on 2022-08-28 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ayede330hourlyreadings", "0011_alter_ayede330hourlyreading_station"),
    ]

    operations = [
        migrations.CreateModel(
            name="Ayede330GoogleSheets",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("google_sheet_title", models.CharField(max_length=30)),
                ("google_sheet_id", models.CharField(max_length=40)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
