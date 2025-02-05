# Generated by Django 5.1.5 on 2025-02-04 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scanner', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scanfile',
            name='file_size',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='scanfile',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='scanfile',
            name='sha_256',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='scanfile',
            name='status',
            field=models.IntegerField(blank=True, choices=[(1, 'infected'), (0, 'Clean')], null=True),
        ),
    ]
