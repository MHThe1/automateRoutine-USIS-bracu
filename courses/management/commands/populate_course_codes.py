from django.core.management.base import BaseCommand
from courses.models import CourseSection
import json
import os

class Command(BaseCommand):
    help = 'Exports the course data to a Python file'

    def handle(self, *args, **kwargs):
        unique_course_codes = CourseSection.objects.values('courseCode').distinct()

        data_to_store = {}

        for course in unique_course_codes:
            course_code = course['courseCode']
            sections = CourseSection.objects.filter(courseCode=course_code).values('courseDetails').distinct()

            data_to_store[course_code] = [section['courseDetails'] for section in sections]

        file_path = os.path.join('courses', 'course_data.py')
        with open(file_path, 'w') as file:
            file.write(f"course_data = {json.dumps(data_to_store, indent=4)}")

        self.stdout.write(self.style.SUCCESS('Successfully exported course data to course_data.py'))
