# Generated by Django 3.2.4 on 2021-07-15 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0005_grade_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiztaker',
            name='grade',
            field=models.ManyToManyField(blank=True, null=True, to='assessment.Grade'),
        ),
        migrations.AlterField(
            model_name='quiztaker',
            name='quiz',
            field=models.ManyToManyField(blank=True, null=True, to='assessment.Quiz'),
        ),
    ]
