# Generated by Django 5.1.6 on 2025-02-17 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_mosque_admin',
            field=models.BooleanField(default=False),
        ),
    ]
