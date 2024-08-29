from django.core.management.base import BaseCommand
from courses.models import CourseSection, CourseCode, CourseSectionInfo

class Command(BaseCommand):
    help = 'Populates the CourseCode and CourseSectionInfo models with data from CourseSection'

    def handle(self, *args, **kwargs):
        # Get all unique course codes from CourseSection
        unique_course_codes = CourseSection.objects.values('courseCode').distinct()

        for course in unique_course_codes:
            course_code, created = CourseCode.objects.get_or_create(courseCode=course['courseCode'])

            # Get all sections for this course code
            sections = CourseSection.objects.filter(courseCode=course_code.courseCode).values('courseDetails').distinct()

            for section in sections:
                CourseSectionInfo.objects.get_or_create(courseCode=course_code, sectionInfo=section['courseDetails'])

        self.stdout.write(self.style.SUCCESS('Successfully populated CourseCode and CourseSectionInfo models'))
