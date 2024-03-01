# Generated by Django 3.2.24 on 2024-03-01 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('degree', '0006_auto_20240229_1903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dockedcourse',
            name='full_code',
            field=models.CharField(blank=True, db_index=True, help_text='The dash-joined department and code of the course, e.g., `CIS-120`', max_length=16),
        ),
    ]
