# Generated by Django 4.1.7 on 2023-04-10 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('placement_app', '0006_student_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='student_gpa',
            name='cgpa',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=3),
        ),
    ]
