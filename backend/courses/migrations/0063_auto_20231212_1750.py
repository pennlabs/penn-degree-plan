# Generated by Django 3.2.23 on 2023-12-12 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0062_alter_section_activity"),
    ]

    operations = [
        migrations.AddField(
            model_name="section",
            name="code_specific_capacity",
            field=models.IntegerField(
                default=0,
                help_text="\nThe max allowed enrollment for this specific section,\nNOT including crosslisted sections.\nThis field is not usable for courses before 2022B\n(first semester after the Path transition).\n",
            ),
        ),
        migrations.AddField(
            model_name="section",
            name="code_specific_enrollment",
            field=models.IntegerField(
                default=0,
                help_text="\nThe number students enrolled in this specific section as of our last registrarimport,\nNOT including crosslisted sections. Comparable with `.code_specific_capacity`.\nThis field is not usable for courses before 2022B\n(first semester after the Path transition).\n",
            ),
        ),
        migrations.AddField(
            model_name="section",
            name="enrollment",
            field=models.IntegerField(
                default=0,
                help_text="\nThe number students enrolled in all crosslistings of this section,\nas of our last registrarimport. Comparable with `.capacity`.\nSOFT STATE, recomputed by `recompute_soft_state` after each registrarimport as\nthe sum of `.code_specific_enrollment` across all crosslisted sections.\nThis field is not usable for courses before 2022B\n(first semester after the Path transition).\n",
            ),
        ),
        migrations.AlterField(
            model_name="instructor",
            name="name",
            field=models.CharField(
                db_index=True, help_text="The full name of the instructor.", max_length=255
            ),
        ),
        migrations.AlterField(
            model_name="section",
            name="capacity",
            field=models.IntegerField(
                default=0,
                help_text="The max allowed enrollment across all crosslistings of this section.",
            ),
        ),
    ]