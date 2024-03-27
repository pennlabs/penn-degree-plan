# Generated by Django 3.1.1 on 2020-10-02 11:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import courses.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("courses", "0029_auto_20200512_1525"),
    ]

    operations = [
        migrations.AlterField(
            model_name="building",
            name="code",
            field=models.CharField(
                help_text="\nThe building code, for instance 570 for the Towne Building. To find the building code\nof a certain building, visit the [Penn Facilities Website](https://bit.ly/2BfE2FE).\n",
                max_length=4,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="building",
            name="latitude",
            field=models.FloatField(
                blank=True,
                help_text="\nThe latitude of the building, in the signed decimal degrees format (global range of\n[-90.0, 90.0]), e.g. 39.961380 for the Towne Building.\n",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="building",
            name="longitude",
            field=models.FloatField(
                blank=True,
                help_text="\nThe longitude of the building, in the signed decimal degrees format (global range of\n[-180.0, 180.0]), e.g. -75.176773 for the Towne Building.\n",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="building",
            name="name",
            field=models.CharField(
                blank=True,
                help_text="\nThe name of the building, for instance 'Towne Building' for the Towne Building. For a\nlist of building names, visit the [Penn Facilities Website](https://bit.ly/2BfE2FE).\n",
                max_length=80,
            ),
        ),
        migrations.AlterField(
            model_name="course",
            name="code",
            field=models.CharField(
                db_index=True, help_text="The course code, e.g. '120' for CIS-120.", max_length=8
            ),
        ),
        migrations.AlterField(
            model_name="course",
            name="department",
            field=models.ForeignKey(
                help_text="\nThe Department object to which the course belongs, e.g. the CIS Department object\nfor CIS-120.\n",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="courses",
                to="courses.department",
            ),
        ),
        migrations.AlterField(
            model_name="course",
            name="description",
            field=models.TextField(
                blank=True,
                help_text="\nThe description of the course, e.g. 'A fast-paced introduction to the fundamental concepts\nof programming... [etc.]' for CIS-120.\n",
            ),
        ),
        migrations.AlterField(
            model_name="course",
            name="full_code",
            field=models.CharField(
                blank=True,
                db_index=True,
                help_text="The dash-joined department and code of the course, e.g. 'CIS-120' for CIS-120.",
                max_length=16,
            ),
        ),
        migrations.AlterField(
            model_name="course",
            name="prerequisites",
            field=models.TextField(
                blank=True,
                help_text="Text describing the prereqs for a course, e.g. 'CIS 120, 160' for CIS-121.",
            ),
        ),
        migrations.AlterField(
            model_name="course",
            name="primary_listing",
            field=models.ForeignKey(
                blank=True,
                help_text="\nThe primary Course object with which this course is crosslisted (all crosslisted courses\nhave a primary listing). The set of crosslisted courses to which this course belongs can\nthus be accessed with the related field listing_set on the primary_listing course.\n",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="listing_set",
                to="courses.course",
            ),
        ),
        migrations.AlterField(
            model_name="course",
            name="semester",
            field=models.CharField(
                db_index=True,
                help_text="\nThe semester of the course (of the form YYYYx where x is A [for spring],\nB [summer], or C [fall]), e.g. 2019C for fall 2019.\n",
                max_length=5,
            ),
        ),
        migrations.AlterField(
            model_name="course",
            name="title",
            field=models.TextField(
                help_text="\nThe title of the course, e.g. 'Programming Languages and Techniques I' for CIS-120.\n"
            ),
        ),
        migrations.AlterField(
            model_name="department",
            name="code",
            field=models.CharField(
                db_index=True,
                help_text="The department code, e.g. 'CIS' for the CIS department.",
                max_length=8,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="department",
            name="name",
            field=models.CharField(
                help_text="\nThe name of the department, e.g. 'Computer and Information Sci' for the CIS department.\n",
                max_length=255,
            ),
        ),
        migrations.AlterField(
            model_name="instructor",
            name="name",
            field=models.CharField(
                db_index=True,
                help_text="The full name of the instructor.",
                max_length=255,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="instructor",
            name="user",
            field=models.ForeignKey(
                blank=True,
                help_text="The instructor's Penn Labs Accounts User object.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="meeting",
            name="day",
            field=models.CharField(
                help_text="The single day on which the meeting takes place (one of M, T, W, R, or F).",
                max_length=1,
            ),
        ),
        migrations.AlterField(
            model_name="meeting",
            name="end",
            field=models.DecimalField(
                decimal_places=2,
                help_text="The end time of the meeting; hh:mm is formatted as hh.mm = h+mm/100.",
                max_digits=4,
            ),
        ),
        migrations.AlterField(
            model_name="meeting",
            name="room",
            field=models.ForeignKey(
                help_text="The Room object in which the meeting is taking place.",
                on_delete=django.db.models.deletion.CASCADE,
                to="courses.room",
            ),
        ),
        migrations.AlterField(
            model_name="meeting",
            name="section",
            field=models.ForeignKey(
                help_text="The Section object to which this class meeting belongs.",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="meetings",
                to="courses.section",
            ),
        ),
        migrations.AlterField(
            model_name="meeting",
            name="start",
            field=models.DecimalField(
                decimal_places=2,
                help_text="The start time of the meeting; hh:mm is formatted as hh.mm = h+mm/100.",
                max_digits=4,
            ),
        ),
        migrations.AlterField(
            model_name="requirement",
            name="code",
            field=models.CharField(
                db_index=True,
                help_text="\nThe code identifying this requirement, e.g. 'MFR' for 'Formal Reasoning Course',\nan SAS requirement satisfied by CIS-120.\n",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="requirement",
            name="courses",
            field=models.ManyToManyField(
                blank=True,
                help_text="\n        Individual Course objects which satisfy this requirement (not necessarily\n        comprehensive, as often entire departments will satisfy the requirement, but not\n        every course in the department will necessarily be added to this set). For example,\n        CIS 398 would be in the courses set for the NATSCI engineering requirement, since\n        it is the only CIS class that satisfies that requirement.\n\nNote that a course satisfies a requirement if and only if it is not in the\noverrides set, and it is either in the courses set or its department is in the departments\nset.\n",
                related_name="requirement_set",
                to="courses.Course",
            ),
        ),
        migrations.AlterField(
            model_name="requirement",
            name="departments",
            field=models.ManyToManyField(
                blank=True,
                help_text="\n        All the Department objects for which any course in that department\n        (if not in overrides) would satisfy this requirement. Usually if a whole department\n        satisfies a requirement, individual courses from that department will not be added to\n        the courses set. Also, to specify specific courses which do not satisfy the requirement\n        (even if their department is in the departments set), the overrides set is used.\n        For example, CIS classes count as engineering (ENG) courses, but CIS-125 is NOT an\n        engineering class, so for the ENG requirement, CIS-125 would be in the overrides\n        set even though the CIS Department object would be in the departments set.\n\nNote that a course satisfies a requirement if and only if it is not in the\noverrides set, and it is either in the courses set or its department is in the departments\nset.\n",
                related_name="requirements",
                to="courses.Department",
            ),
        ),
        migrations.AlterField(
            model_name="requirement",
            name="name",
            field=models.CharField(
                help_text="\nThe name of the requirement, e.g. 'Formal Reasoning Course', an SAS requirement\nsatisfied by CIS-120.\n",
                max_length=255,
            ),
        ),
        migrations.AlterField(
            model_name="requirement",
            name="overrides",
            field=models.ManyToManyField(
                blank=True,
                help_text="\n        Individual Course objects which do not satisfy this requirement. This set\n        is usually used to add exceptions to departments which satisfy requirements.\n        For example, CIS classes count as engineering (ENG) courses, but CIS-125 is NOT an\n        engineering class, so for the ENG requirement, CIS-125 would be in the overrides\n        set even though the CIS Department would be in the departments set.\n\nNote that a course satisfies a requirement if and only if it is not in the\noverrides set, and it is either in the courses set or its department is in the departments\nset.\n",
                related_name="nonrequirement_set",
                to="courses.Course",
            ),
        ),
        migrations.AlterField(
            model_name="requirement",
            name="school",
            field=models.CharField(
                choices=[("SEAS", "Engineering"), ("WH", "Wharton"), ("SAS", "College")],
                db_index=True,
                help_text='\nWhat school this requirement belongs to, e.g. \'SAS\' for the SAS \'Formal Reasoning Course\'\nrequirement satisfied by CIS-120. Options and meanings:\n<table width=100%><tr><td>"SEAS"</td><td>"Engineering"</td></tr><tr><td>"WH"</td><td>"Wharton"</td></tr><tr><td>"SAS"</td><td>"College"</td></tr></table>',
                max_length=5,
            ),
        ),
        migrations.AlterField(
            model_name="requirement",
            name="semester",
            field=models.CharField(
                db_index=True,
                help_text="\nThe semester of the requirement (of the form YYYYx where x is A [for spring], B [summer],\nor C [fall]), e.g. 2019C for fall 2019. We organize requirements by semester so that we\ndon't get huge related sets which don't give particularly good info.\n",
                max_length=5,
            ),
        ),
        migrations.AlterField(
            model_name="restriction",
            name="code",
            field=models.CharField(
                help_text="\nA registration restriction control code, for instance 'PDP' for CIS-121 (permission\nrequired from dept for registration). See [bit.ly/3eu17m2](https://bit.ly/3eu17m2)\nfor all options.\n",
                max_length=10,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="restriction",
            name="description",
            field=models.TextField(
                help_text="\nThe registration restriction description, e.g. 'Permission Needed From Department'\nfor the PDP restriction (on CIS-121, for example). See\n[bit.ly/3eu17m2](https://bit.ly/3eu17m2) for all options.\n"
            ),
        ),
        migrations.AlterField(
            model_name="room",
            name="building",
            field=models.ForeignKey(
                help_text="\nThe Building object in which the room is located, e.g. the Levine Hall Building\nobject for Wu and Chen Auditorium (rm 101).\n",
                on_delete=django.db.models.deletion.CASCADE,
                to="courses.building",
            ),
        ),
        migrations.AlterField(
            model_name="room",
            name="name",
            field=models.CharField(
                help_text="The room name (optional, empty string if none), e.g. 'Wu and Chen Auditorium'.",
                max_length=80,
            ),
        ),
        migrations.AlterField(
            model_name="room",
            name="number",
            field=models.CharField(
                help_text="The room number, e.g. 101 for Wu and Chen Auditorium in Levine.",
                max_length=5,
            ),
        ),
        migrations.AlterField(
            model_name="section",
            name="activity",
            field=models.CharField(
                choices=[
                    ("CLN", "Clinic"),
                    ("DIS", "Dissertation"),
                    ("IND", "Independent Study"),
                    ("LAB", "Lab"),
                    ("LEC", "Lecture"),
                    ("MST", "Masters Thesis"),
                    ("REC", "Recitation"),
                    ("SEM", "Seminar"),
                    ("SRT", "Senior Thesis"),
                    ("STU", "Studio"),
                    ("***", "Undefined"),
                ],
                db_index=True,
                help_text='The section activity, e.g. \'LEC\' for CIS-120-001 (2020A). Options and meanings: <table width=100%><tr><td>"CLN"</td><td>"Clinic"</td></tr><tr><td>"DIS"</td><td>"Dissertation"</td></tr><tr><td>"IND"</td><td>"Independent Study"</td></tr><tr><td>"LAB"</td><td>"Lab"</td></tr><tr><td>"LEC"</td><td>"Lecture"</td></tr><tr><td>"MST"</td><td>"Masters Thesis"</td></tr><tr><td>"REC"</td><td>"Recitation"</td></tr><tr><td>"SEM"</td><td>"Seminar"</td></tr><tr><td>"SRT"</td><td>"Senior Thesis"</td></tr><tr><td>"STU"</td><td>"Studio"</td></tr><tr><td>"***"</td><td>"Undefined"</td></tr></table>',
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="section",
            name="associated_sections",
            field=models.ManyToManyField(
                help_text="\nA list of all sections associated with the Course which this section belongs to; e.g. for\nCIS-120-001, all of the lecture and recitation sections for CIS-120 (including CIS-120-001)\nin the same semester.\n",
                to="courses.Section",
            ),
        ),
        migrations.AlterField(
            model_name="section",
            name="capacity",
            field=models.IntegerField(
                default=0,
                help_text="The number of allowed registrations for this section, e.g. 220 for CIS-120-001 (2020A).",
            ),
        ),
        migrations.AlterField(
            model_name="section",
            name="code",
            field=models.CharField(
                db_index=True,
                help_text="The section code, e.g. '001' for the section CIS-120-001.",
                max_length=16,
            ),
        ),
        migrations.AlterField(
            model_name="section",
            name="course",
            field=models.ForeignKey(
                help_text="\nThe Course object to which this section belongs, e.g. the CIS-120 Course object for\nCIS-120-001.\n",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sections",
                to="courses.course",
            ),
        ),
        migrations.AlterField(
            model_name="section",
            name="credits",
            field=models.DecimalField(
                blank=True,
                db_index=True,
                decimal_places=2,
                help_text="The number of credits this section is worth.",
                max_digits=3,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="section",
            name="full_code",
            field=models.CharField(
                blank=True,
                db_index=True,
                help_text="\nThe full code of the section, in the form '{dept code}-{course code}-{section code}',\ne.g. 'CIS-120-001' for the 001 section of CIS-120.\n",
                max_length=32,
            ),
        ),
        migrations.AlterField(
            model_name="section",
            name="instructors",
            field=models.ManyToManyField(
                help_text="The Instructor object(s) of the instructor(s) teaching the section.",
                to="courses.Instructor",
            ),
        ),
        migrations.AlterField(
            model_name="section",
            name="meeting_times",
            field=models.TextField(
                blank=True,
                help_text='\nA JSON-stringified list of meeting times of the form\n\'{days code} {start time} - {end time}\', e.g.\n\'["MWF 09:00 AM - 10:00 AM","F 11:00 AM - 12:00 PM","T 05:00 PM - 06:00 PM"]\' for\nPHYS-151-001 (2020A). Each letter of the days code is of the form M, T, W, R, F for each\nday of the work week, respectively (and multiple days are combined with concatenation).\nTo access the Meeting objects for this section, the related field `meetings` can be used.\n',
            ),
        ),
        migrations.AlterField(
            model_name="section",
            name="restrictions",
            field=models.ManyToManyField(
                blank=True,
                help_text="All registration Restriction objects to which this section is subject.",
                to="courses.Restriction",
            ),
        ),
        migrations.AlterField(
            model_name="section",
            name="status",
            field=models.CharField(
                choices=[("O", "Open"), ("C", "Closed"), ("X", "Cancelled"), ("", "Unlisted")],
                db_index=True,
                help_text='The registration status of the section. Options and meanings: <table width=100%><tr><td>"O"</td><td>"Open"</td></tr><tr><td>"C"</td><td>"Closed"</td></tr><tr><td>"X"</td><td>"Cancelled"</td></tr><tr><td>""</td><td>"Unlisted"</td></tr></table>',
                max_length=4,
            ),
        ),
        migrations.AlterField(
            model_name="statusupdate",
            name="alert_sent",
            field=models.BooleanField(
                help_text="Was an alert was sent to a User as a result of this status update?"
            ),
        ),
        migrations.AlterField(
            model_name="statusupdate",
            name="new_status",
            field=models.CharField(
                choices=[("O", "Open"), ("C", "Closed"), ("X", "Cancelled"), ("", "Unlisted")],
                help_text='The new status code (to which the section changed). Options and meanings: <table width=100%><tr><td>"O"</td><td>"Open"</td></tr><tr><td>"C"</td><td>"Closed"</td></tr><tr><td>"X"</td><td>"Cancelled"</td></tr><tr><td>""</td><td>"Unlisted"</td></tr></table>',
                max_length=16,
            ),
        ),
        migrations.AlterField(
            model_name="statusupdate",
            name="old_status",
            field=models.CharField(
                choices=[("O", "Open"), ("C", "Closed"), ("X", "Cancelled"), ("", "Unlisted")],
                help_text='The old status code (from which the section changed). Options and meanings: <table width=100%><tr><td>"O"</td><td>"Open"</td></tr><tr><td>"C"</td><td>"Closed"</td></tr><tr><td>"X"</td><td>"Cancelled"</td></tr><tr><td>""</td><td>"Unlisted"</td></tr></table>',
                max_length=16,
            ),
        ),
        migrations.AlterField(
            model_name="statusupdate",
            name="section",
            field=models.ForeignKey(
                help_text="The section which this status update applies to.",
                on_delete=django.db.models.deletion.CASCADE,
                to="courses.section",
            ),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="email",
            field=models.EmailField(
                blank=True,
                help_text="The email of the User. Defaults to null.",
                max_length=254,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="phone",
            field=models.CharField(
                blank=True,
                help_text="\nThe phone number of the user. Defaults to null.\nThe phone number will be stored in the E164 format, but any form parseable by the\n[phonenumbers library](https://pypi.org/project/phonenumbers/)\nwill be accepted and converted to E164 format automatically upon saving.\n",
                max_length=100,
                null=True,
                validators=[courses.models.UserProfile.validate_phone],
            ),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="user",
            field=models.OneToOneField(
                help_text="The User object to which this User Profile object belongs.",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="profile",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
