# Generated by Django 2.2.5 on 2019-09-28 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0019_apikey_apiprivilege"),
    ]

    operations = [
        migrations.AlterField(
            model_name="apikey",
            name="privileges",
            field=models.ManyToManyField(
                blank=True, related_name="key_set", to="courses.APIPrivilege"
            ),
        ),
    ]
