# Generated by Django 5.1 on 2024-10-17 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vcs', '0002_repositoryfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repositoryfile',
            name='file',
            field=models.FileField(max_length=1000, upload_to='repositories/'),
        ),
        migrations.AlterField(
            model_name='repositoryfile',
            name='path',
            field=models.CharField(max_length=1000),
        ),
    ]