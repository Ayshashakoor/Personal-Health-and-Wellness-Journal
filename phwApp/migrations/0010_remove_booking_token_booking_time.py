# Generated by Django 4.2.7 on 2024-03-19 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phwApp', '0009_alter_doctor_qualification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='token',
        ),
        migrations.AddField(
            model_name='booking',
            name='time',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
