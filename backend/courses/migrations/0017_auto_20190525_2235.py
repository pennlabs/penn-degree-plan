# Generated by Django 2.2.1 on 2019-05-25 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0016_auto_20190523_1554"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="full_code",
            field=models.CharField(blank=True, max_length=16),
        ),
        migrations.AlterUniqueTogether(
            name="course",
            unique_together={("full_code", "semester"), ("department", "code", "semester")},
        ),
    ]
