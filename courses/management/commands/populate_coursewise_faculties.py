from django.core.management.base import BaseCommand
from courses.models import CourseSection
import os

class Command(BaseCommand):
    help = 'Exports faculty data to a Python file in the courses app'

    def handle(self, *args, **kwargs):
        faculties = {}

        course_sections = CourseSection.objects.all().values('courseCode', 'empShortName')

        for course in course_sections:
            course_code = course['courseCode']
            emp_short_name = course['empShortName']

            if course_code not in faculties:
                faculties[course_code] = []

            if emp_short_name not in faculties[course_code]:
                faculties[course_code].append(emp_short_name)

        file_path = os.path.join('courses', 'faculties_data.py')

        with open(file_path, 'w') as file:
            file.write(f'faculties = {faculties}\n')

        self.stdout.write(self.style.SUCCESS(f'Successfully exported faculties data to {file_path}'))
