# Generated by Django 2.2 on 2019-04-28 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0003_auto_20190428_1707"),
    ]

    operations = [
        migrations.RenameField(
            model_name="room",
            old_name="roomnum",
            new_name="number",
        ),
        migrations.AlterField(
            model_name="building",
            name="code",
            field=models.CharField(max_length=4, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name="room",
            unique_together={("building", "number")},
        ),
    ]
