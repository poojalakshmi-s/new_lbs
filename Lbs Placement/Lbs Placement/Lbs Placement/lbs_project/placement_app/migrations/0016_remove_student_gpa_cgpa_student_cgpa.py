# Generated by Django 4.1.7 on 2023-04-11 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('placement_app', '0015_student_gpa_cgpa'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student_gpa',
            name='cgpa',
        ),
        migrations.AddField(
            model_name='student',
            name='cgpa',
            field=models.FloatField(default=0, max_length=100),
        ),
    ]
