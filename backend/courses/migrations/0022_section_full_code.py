# Generated by Django 2.2.6 on 2019-11-01 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0021_auto_20191019_2140"),
    ]

    operations = [
        migrations.AddField(
            model_name="section",
            name="full_code",
            field=models.CharField(blank=True, max_length=32),
        ),
    ]