# Generated by Django 5.1.7 on 2025-03-28 14:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_remove_schedule_event_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='event_description',
        ),
    ]
