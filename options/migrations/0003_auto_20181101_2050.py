# Generated by Django 2.1.3 on 2018-11-01 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("options", "0002_auto_20181101_0047"),
    ]

    operations = [
        migrations.AlterField(
            model_name="option",
            name="value_type",
            field=models.CharField(
                choices=[("TXT", "Text"), ("INT", "Integer"), ("BOOL", "Boolean")],
                default="TXT",
                max_length=8,
            ),
        ),
    ]
