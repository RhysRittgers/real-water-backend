# Generated by Django 5.1.7 on 2025-03-28 14:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_schedule_jugs_per_delivery'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='event_name',
        ),
    ]
