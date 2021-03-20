# Generated by Django 3.2b1 on 2021-03-20 18:14

import alert.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alert', '0012_auto_20210319_0228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adddropperiod',
            name='semester',
            field=models.CharField(db_index=True, help_text='\nThe semester of this add drop period (of the form YYYYx where x is\nA [for spring], or C [fall]), e.g. 2019C for fall 2019.\n', max_length=5, unique=True, validators=[alert.models.validate_add_drop_semester]),
        ),
        migrations.AlterField(
            model_name='pcademandextrema',
            name='semester',
            field=models.CharField(db_index=True, help_text='\nThe semester of this demand extrema (of the form YYYYx where x is\nA [for spring], B [summer], or C [fall]), e.g. 2019C for fall 2019.\n', max_length=5),
        ),
    ]
