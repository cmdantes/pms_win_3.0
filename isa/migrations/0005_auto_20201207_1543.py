# Generated by Django 3.1.3 on 2020-12-07 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('isa', '0004_auto_20201207_1540'),
    ]

    operations = [




        migrations.AddField(
            model_name='tblpermit',
            name='vatreg',
            field=models.CharField(blank=True, db_column='VATReg', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='tblpermit',
            name='id',
            field=models.BigAutoField(db_column='ID', primary_key=True, serialize=False),
        ),
    ]
