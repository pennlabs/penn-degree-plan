# Generated by Django 4.0.5 on 2022-08-28 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("plan", "0005_primaryscheduleloookup"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="primaryscheduleloookup",
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name="primaryscheduleloookup",
            name="person",
        ),
        migrations.RemoveField(
            model_name="primaryscheduleloookup",
            name="schedule",
        ),
        migrations.AddField(
            model_name="schedule",
            name="is_shared",
            field=models.BooleanField(
                default=False,
                help_text="This determines whether this schedule is sharable with the user's friends",
            ),
        ),
        migrations.AddConstraint(
            model_name="schedule",
            constraint=models.UniqueConstraint(
                condition=models.Q(("is_shared", True)),
                fields=("person_id",),
                name="max_one_shared_per_person",
            ),
        ),
        migrations.DeleteModel(
            name="PrimaryScheduleLoookup",
        ),
    ]