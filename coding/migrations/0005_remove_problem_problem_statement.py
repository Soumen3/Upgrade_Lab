# Generated by Django 5.1 on 2024-10-19 10:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coding', '0004_codesnippet'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='problem_statement',
        ),
    ]
