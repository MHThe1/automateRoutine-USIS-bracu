# Generated by Django 5.1 on 2024-09-12 06:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CourseCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courseCode', models.CharField(max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CourseSection',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('academicSectionId', models.IntegerField()),
                ('courseId', models.IntegerField()),
                ('academicSessionId', models.IntegerField()),
                ('courseCode', models.CharField(max_length=10)),
                ('courseTitle', models.CharField(max_length=255)),
                ('courseDetails', models.CharField(max_length=255)),
                ('empName', models.CharField(max_length=255)),
                ('empShortName', models.CharField(max_length=10)),
                ('deptName', models.CharField(max_length=255)),
                ('classSchedule', models.TextField()),
                ('classLabSchedule', models.TextField()),
                ('preRequisiteCourses', models.TextField(blank=True)),
                ('defaultSeatCapacity', models.IntegerField()),
                ('availableSeat', models.IntegerField()),
                ('totalFillupSeat', models.IntegerField()),
                ('courseCredit', models.DecimalField(decimal_places=1, max_digits=3)),
                ('dayNo', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='CourseSectionInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sectionInfo', models.CharField(max_length=20)),
                ('courseCode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='courses.coursecode')),
            ],
        ),
    ]
