# Generated by Django 5.0.6 on 2024-07-04 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('vacancy_name', models.CharField(max_length=255)),
                ('archived', models.BooleanField()),
                ('area', models.CharField(max_length=255)),
                ('contact_information', models.CharField(max_length=255)),
                ('metro', models.CharField(max_length=255)),
                ('salary', models.CharField(max_length=255)),
                ('schedule', models.CharField(max_length=255)),
                ('counters', models.IntegerField()),
                ('employement', models.CharField(max_length=255)),
                ('experience', models.CharField(max_length=255)),
                ('published_at', models.DateTimeField()),
                ('url', models.CharField(max_length=255)),
            ],
        ),
    ]