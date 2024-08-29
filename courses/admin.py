from django.contrib import admin
from courses.models import CourseSection, CourseCode, CourseSectionInfo

# Register your models here.

admin.site.register(CourseSection)
admin.site.register(CourseCode)
admin.site.register(CourseSectionInfo)