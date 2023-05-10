# Generated by Django 4.1.7 on 2023-04-27 11:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('placement_app', '0025_jobpostapplication_company_ids'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobpostapplication',
            name='company_ids',
        ),
        migrations.CreateModel(
            name='Schedule_Interview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interview_scheduled', models.DateTimeField()),
                ('instructions', models.CharField(default='', max_length=10000)),
                ('interview_link', models.CharField(default='', max_length=100)),
                ('interview_mode', models.CharField(default='', max_length=100)),
                ('job_post_idss', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='placement_app.jobpostapplication')),
            ],
        ),
    ]