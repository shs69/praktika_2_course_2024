# Generated by Django 5.0.6 on 2024-07-04 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job_parser', '0003_rename_contact_information_vacancy_information_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vacancy',
            old_name='employement',
            new_name='employment',
        ),
    ]