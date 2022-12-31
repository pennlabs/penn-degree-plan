# Generated by Django 2.2.1 on 2019-05-18 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0013_auto_20190517_0313"),
    ]

    operations = [
        migrations.AlterField(
            model_name="requirement",
            name="school",
            field=models.CharField(
                choices=[
                    ("SEAS", "Engineering"),
                    ("WH", "Wharton"),
                    ("SAS", "College"),
                ],
                max_length=5,
            ),
        ),
        migrations.AlterUniqueTogether(
            name="requirement",
            unique_together={("semester", "code", "school")},
        ),
    ]
