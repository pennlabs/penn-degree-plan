# Generated by Django 2.2.5 on 2019-09-26 05:49

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0018_merge_20190526_1901'),
    ]

    operations = [
        migrations.CreateModel(
            name='APIPrivilege',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='APIKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('code', models.CharField(blank=True, default=uuid.uuid4, max_length=100, unique=True)),
                ('active', models.BooleanField(blank=True, default=True)),
                ('privileges', models.ManyToManyField(related_name='key_set', to='courses.APIPrivilege')),
            ],
        ),
    ]