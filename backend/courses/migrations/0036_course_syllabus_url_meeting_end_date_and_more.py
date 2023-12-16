# Generated by Django 4.0.3 on 2022-04-04 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0035_topic_course_topic"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="syllabus_url",
            field=models.TextField(
                blank=True,
                help_text="\nA URL for the syllabus of the course, if available.\nNot available for courses offered in or before spring 2022.\n",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="meeting",
            name="end_date",
            field=models.TextField(
                blank=True,
                help_text="\nThe last day this meeting takes place, in the form 'YYYY-MM-DD', e.g. '2022-12-12'.\nNot available for sections offered in or before spring 2022.\n",
                max_length=10,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="meeting",
            name="start_date",
            field=models.TextField(
                blank=True,
                help_text="\nThe first day this meeting takes place, in the form 'YYYY-MM-DD', e.g. '2022-08-30'.\nNot available for sections offered in or before spring 2022.\n",
                max_length=10,
                null=True,
            ),
        ),
    ]
