# Generated by Django 3.2.23 on 2024-03-27 06:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Degree',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('program', models.CharField(choices=[('EU_BSE', 'Engineering BSE'), ('EU_BAS', 'Engineering BAS'), ('AU_BA', 'College BA'), ('WU_BS', 'Wharton BS'), ('NU_BSN', 'Nursing BSN')], help_text='\nThe program code for this degree, e.g., EU_BSE\n', max_length=10)),
                ('degree', models.CharField(help_text='\nThe degree code for this degree, e.g., BSE\n', max_length=4)),
                ('major', models.CharField(help_text='\nThe major code for this degree, e.g., BIOL\n', max_length=4)),
                ('concentration', models.CharField(help_text='\nThe concentration code for this degree, e.g., BMAT\n', max_length=4, null=True)),
                ('year', models.IntegerField(help_text='\nThe effective year of this degree, e.g., 2023\n')),
                ('credits', models.DecimalField(decimal_places=2, help_text='\nThe minimum number of CUs required for this degree.\n', max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='DegreePlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text="The user's nickname for the degree plan.", max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('degrees', models.ManyToManyField(blank=True, help_text='The degrees this degree plan is associated with.', to='degree.Degree')),
                ('person', models.ForeignKey(help_text='The user the degree plan belongs to.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, help_text='\nThe title for this rule.\n', max_length=200)),
                ('num', models.PositiveSmallIntegerField(help_text='\nThe minimum number of courses or subrules required for this rule.\n', null=True)),
                ('credits', models.DecimalField(decimal_places=2, help_text='\nThe minimum number of CUs required for this rule. Only non-null\nif this is a Rule leaf.\n', max_digits=4, null=True)),
                ('q', models.TextField(blank=True, help_text='\nString representing a Q() object that returns the set of courses\nsatisfying this rule. Non-empty iff this is a Rule leaf.\nThis Q object is expected to be normalized before it is serialized\nto a string.\n', max_length=1000)),
                ('parent', models.ForeignKey(help_text="\nThis rule's parent Rule if it has one. Null if this is a top level rule\n(i.e., this rule belongs to some Degree's `.rules` set).\n", null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='degree.rule')),
            ],
        ),
        migrations.CreateModel(
            name='SatisfactionStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('satisfied', models.BooleanField(default=False, help_text='Whether the rule is satisfied')),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('last_checked', models.DateTimeField(default=django.utils.timezone.now)),
                ('degree_plan', models.ForeignKey(help_text='The degree plan that leads to the satisfaction of the rule', on_delete=django.db.models.deletion.CASCADE, related_name='satisfactions', to='degree.degreeplan')),
                ('rule', models.ForeignKey(help_text='The rule that is satisfied', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='degree.rule')),
            ],
        ),
        migrations.CreateModel(
            name='PDPBetaUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('person', models.ForeignKey(help_text='The user who has access to the PDP beta', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Fulfillment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_code', models.CharField(blank=True, db_index=True, help_text='The dash-joined department and code of the course, e.g., `CIS-120`', max_length=16)),
                ('semester', models.CharField(help_text='\nThe semester of the course (of the form YYYYx where x is A [for spring],\nB [summer], or C [fall]), e.g. `2019C` for fall 2019. Null if this fulfillment\ndoes not yet have a semester.\n', max_length=5, null=True)),
                ('degree_plan', models.ForeignKey(help_text='The degree plan with which this fulfillment is associated', on_delete=django.db.models.deletion.CASCADE, related_name='fulfillments', to='degree.degreeplan')),
                ('rules', models.ManyToManyField(blank=True, help_text='\nThe rules this course fulfills. Blank if this course does not apply\nto any rules.\n', related_name='_degree_fulfillment_rules_+', to='degree.Rule')),
            ],
        ),
        migrations.CreateModel(
            name='DoubleCountRestriction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_courses', models.PositiveSmallIntegerField(help_text='\nThe maximum number of courses you can count for both rules.\nIf null, there is no limit, and max_credits must not be null.\n', null=True)),
                ('max_credits', models.DecimalField(decimal_places=2, help_text='\nThe maximum number of CUs you can count for both rules.\nIf null, there is no limit, and max_credits must not be null.\n', max_digits=4, null=True)),
                ('other_rule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='degree.rule')),
                ('rule', models.ForeignKey(help_text='\nA rule in the double count restriction.\n', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='degree.rule')),
            ],
        ),
        migrations.CreateModel(
            name='DockedCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_code', models.CharField(blank=True, db_index=True, help_text='The dash-joined department and code of the course, e.g., `CIS-120`', max_length=16)),
                ('person', models.ForeignKey(help_text='The user the docked course belongs to.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='degree',
            name='rules',
            field=models.ManyToManyField(blank=True, help_text='\nThe rules for this degree. Blank if this degree has no rules.\n', related_name='degrees', to='degree.Rule'),
        ),
        migrations.AddConstraint(
            model_name='satisfactionstatus',
            constraint=models.UniqueConstraint(fields=('degree_plan', 'rule'), name='unique_satisfaction'),
        ),
        migrations.AlterUniqueTogether(
            name='fulfillment',
            unique_together={('degree_plan', 'full_code')},
        ),
        migrations.AddConstraint(
            model_name='dockedcourse',
            constraint=models.UniqueConstraint(fields=('person', 'full_code'), name='unique docked course'),
        ),
        migrations.AddConstraint(
            model_name='degreeplan',
            constraint=models.UniqueConstraint(fields=('name', 'person'), name='degreeplan_name_person'),
        ),
        migrations.AddConstraint(
            model_name='degree',
            constraint=models.UniqueConstraint(fields=('program', 'degree', 'major', 'concentration', 'year'), name='unique degree'),
        ),
    ]
