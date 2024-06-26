# Generated by Django 3.2.23 on 2024-03-27 06:49

from django.db import migrations, models

from courses.management.commands.recompute_soft_state import COURSE_CREDITS_RAW_SQL


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0063_auto_20231212_1750"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="credits",
            field=models.DecimalField(
                blank=True,
                db_index=True,
                decimal_places=2,
                help_text="The number of credits this course takes. This is precomputed for efficiency.",
                max_digits=4,
                null=True,
            ),
        ),
        # Run a backfill on Course.credits
        migrations.RunSQL(
            COURSE_CREDITS_RAW_SQL,
        ),
        migrations.AlterField(
            model_name="course",
            name="num_activities",
            field=models.IntegerField(
                default=0,
                help_text="\nThe number of distinct activities belonging to this course (precomputed for efficiency).\nMaintained by the registrar import / recomputestats script.\n",
            ),
        ),
        migrations.AlterField(
            model_name="section",
            name="activity",
            field=models.CharField(
                choices=[
                    ("", "Undefined"),
                    ("CLN", "Clinic"),
                    ("CRT", "Clinical Rotation"),
                    ("DAB", "Dissertation Abroad"),
                    ("DIS", "Dissertation"),
                    ("DPC", "Doctoral Program Exchange"),
                    ("FLD", "Field Work"),
                    ("HYB", "Hybrid"),
                    ("IND", "Independent Study"),
                    ("LAB", "Lab"),
                    ("LEC", "Lecture"),
                    ("MST", "Masters Thesis"),
                    ("ONL", "Online"),
                    ("PRC", "Practicum"),
                    ("REC", "Recitation"),
                    ("SEM", "Seminar"),
                    ("SRT", "Senior Thesis"),
                    ("STU", "Studio"),
                ],
                db_index=True,
                help_text='The section activity, e.g. `LEC` for CIS-120-001 (2020A). Options and meanings: <table width=100%><tr><td>""</td><td>"Undefined"</td></tr><tr><td>"CLN"</td><td>"Clinic"</td></tr><tr><td>"CRT"</td><td>"Clinical Rotation"</td></tr><tr><td>"DAB"</td><td>"Dissertation Abroad"</td></tr><tr><td>"DIS"</td><td>"Dissertation"</td></tr><tr><td>"DPC"</td><td>"Doctoral Program Exchange"</td></tr><tr><td>"FLD"</td><td>"Field Work"</td></tr><tr><td>"HYB"</td><td>"Hybrid"</td></tr><tr><td>"IND"</td><td>"Independent Study"</td></tr><tr><td>"LAB"</td><td>"Lab"</td></tr><tr><td>"LEC"</td><td>"Lecture"</td></tr><tr><td>"MST"</td><td>"Masters Thesis"</td></tr><tr><td>"ONL"</td><td>"Online"</td></tr><tr><td>"PRC"</td><td>"Practicum"</td></tr><tr><td>"REC"</td><td>"Recitation"</td></tr><tr><td>"SEM"</td><td>"Seminar"</td></tr><tr><td>"SRT"</td><td>"Senior Thesis"</td></tr><tr><td>"STU"</td><td>"Studio"</td></tr></table>',
                max_length=50,
            ),
        ),
    ]
