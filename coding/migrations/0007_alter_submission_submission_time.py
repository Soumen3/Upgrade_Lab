# Generated by Django 5.1 on 2024-10-20 07:19

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coding', '0006_alter_testcase_expected_output_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='submission_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
