# Generated by Django 5.1.7 on 2025-03-28 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_schedule_jug_returns'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='jugs_per_delivery',
            field=models.IntegerField(default=0),
        ),
    ]
