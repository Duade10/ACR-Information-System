# Generated by Django 4.1b1 on 2022-07-20 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("troublereports", "0002_troublereport_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="troublereport",
            name="to_authority",
            field=models.CharField(
                choices=[("pm(so)", "PM(SO)"), ("pm(t)", "PM(T)")], max_length=20
            ),
        ),
    ]
