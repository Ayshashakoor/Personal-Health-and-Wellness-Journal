# Generated by Django 4.2.7 on 2024-02-21 08:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phwApp', '0003_request_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='foodjournals',
            name='time',
        ),
    ]
