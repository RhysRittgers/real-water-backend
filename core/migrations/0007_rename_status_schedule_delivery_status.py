# Generated by Django 5.1.7 on 2025-03-28 14:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_remove_schedule_event_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schedule',
            old_name='status',
            new_name='delivery_status',
        ),
    ]
