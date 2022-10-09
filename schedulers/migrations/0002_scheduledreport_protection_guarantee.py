# Generated by Django 4.0.7 on 2022-08-31 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('protection_guarantees', '0011_protectionguarantee_is_acknowledged'),
        ('schedulers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduledreport',
            name='protection_guarantee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='protection_guarantees.protectionguarantee'),
        ),
    ]
