# Generated by Django 3.1.3 on 2020-12-17 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('isa', '0007_remove_transactionzeroamount_time_stay'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionzeroamount',
            name='time_stay',
            field=models.CharField(blank=True, max_length=45, null=True),
        ),
    ]
