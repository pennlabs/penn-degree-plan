# Generated by Django 3.2.23 on 2024-02-06 00:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('degree', '0005_auto_20240205_0150'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='degreeplan',
            name='degree',
        ),
        migrations.RemoveField(
            model_name='rule',
            name='degree',
        ),
        migrations.AddField(
            model_name='degree',
            name='rules',
            field=models.ManyToManyField(blank=True, help_text='\nThe rules for this degree. Blank if this degree has no rules.\n', related_name='degrees', to='degree.Rule'),
        ),
        migrations.AddField(
            model_name='degreeplan',
            name='degrees',
            field=models.ManyToManyField(help_text='The degree this is associated with.', to='degree.Degree'),
        ),
        migrations.AlterField(
            model_name='rule',
            name='parent',
            field=models.ForeignKey(help_text="\nThis rule's parent Rule if it has one. Null if this is a top level rule\n(i.e., this rule belongs to some Degree's `.rules` set).\n", null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='degree.rule'),
        ),
    ]