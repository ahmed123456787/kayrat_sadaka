# Generated by Django 5.1.6 on 2025-02-27 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_notification_delete_sms_distribution_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='read',
            field=models.BooleanField(default=False),
        ),
    ]
