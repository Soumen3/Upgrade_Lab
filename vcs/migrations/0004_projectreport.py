# Generated by Django 5.1 on 2025-04-14 07:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vcs', '0003_alter_repositoryfile_file_alter_repositoryfile_path'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(max_length=1000, upload_to='project_reports/')),
                ('repository', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='project_report', to='vcs.repository')),
            ],
        ),
    ]
