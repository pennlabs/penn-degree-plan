# Generated by Django 2.2 on 2019-04-28 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0002_auto_20190426_2158"),
    ]

    operations = [
        migrations.AlterField(
            model_name="building", name="latitude", field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="building", name="longitude", field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="building", name="name", field=models.CharField(blank=True, max_length=80),
        ),
    ]
