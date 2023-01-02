# Generated by Django 4.0.1 on 2022-03-30 02:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0034_auto_20211114_0032"),
    ]

    operations = [
        migrations.CreateModel(
            name="Topic",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "branched_from",
                    models.ForeignKey(
                        blank=True,
                        help_text="\nWhen relevant, the Topic from which this Topic was branched (this will likely only be\nuseful for the spring 2022 NGSS course code changes, where some courses were split into\nmultiple new courses of different topics).\n",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="branched_to",
                        to="courses.topic",
                    ),
                ),
                (
                    "most_recent",
                    models.ForeignKey(
                        help_text="\nThe most recent course (by semester) of this topic. The `most_recent` course should\nbe the `primary_listing` if it has crosslistings. These invariants are maintained\nby the `Topic.merge_with`, `Topic.add_course`, `Topic.from_course`, and `Course.save`\nmethods. Defer to using these methods rather than setting this field manually.\nYou must change the corresponding `Topic` object's `most_recent` field before\ndeleting a Course if it is the `most_recent` course (`on_delete=models.PROTECT`).\n",
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="courses.course",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="course",
            name="topic",
            field=models.ForeignKey(
                blank=True,
                help_text="The Topic of this course",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="courses",
                to="courses.topic",
            ),
        ),
    ]
